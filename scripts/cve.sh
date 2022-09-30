#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=cve
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "cve-2021-27421"
)

CONFIGURATIONS=(
    "baseline"
    "randxom-small"
    "randxom-medium"
    "randxom-large"
    "randezvous-small"
    "randezvous-medium"
    "randezvous-large"
)

#
# Load common components.
#
. "$ROOT_DIR/scripts/common.sh"

#
# Redefine the run() function.
#
# $1: the configuration to use.
# $2: the program to run.
# $3: number of seconds between two pairs of actions of feeding an input and
#     getting the output (default 0.6).
# $4: number of control flow targets to skip (default 0).
# $5: initial number of failures (default 0).
# $6: initial number of silences (default 0).
# $7: control data slot breakpoint (default 0).
#
unset run
run() {
    # Find IDE if we have not done so
    if [[ -z "$FLASH_TOOL" ]] || [[ -z "$FLASH_SERVER" ]]; then
        find_ide
    fi

    # Check if necessary variables are defined
    if [[ -z "$CONFIGURATIONS" ]] || [[ -z "$PROGRAMS" ]] ||
       [[ -z "$PROJ" ]] || [[ -z "$PROJ_DIR" ]]; then
        echo "One or more necessary variables undefined!"
        exit 1
    fi
    # Check if the configuration name is valid
    if [[ ! " ${CONFIGURATIONS[@]} " =~ " $1 " ]]; then
        echo "Configuration must be one of the following:"
        echo "${CONFIGURATIONS[@]}"
        exit 1
    fi

    # Check if the program name is valid
    if [[ ! " ${PROGRAMS[@]} " =~ " $2 " ]]; then
        echo "Program must be one of the following:"
        echo "${PROGRAMS[@]}"
        exit 1
    fi

    # Check if the action interval is a good number
    local action_interval=0.6
    if [[ -n "$3" ]]; then
        if [[ "$3" =~ ^([0-9]+\.?[0-9]+|[0-9]*\.[0-9]+)$ ]]; then
            action_interval="$3"
        else
            echo "Invalid number of action interval!"
            exit 1
        fi
    fi

    # Check for breakpoint continuation control
    local skip=0
    local init_failures=0
    local init_silences=0
    local slot_bkpt=0
    if [[ -n "$4" ]]; then
        if [[ "$4" =~ ^[0-9]+$ ]]; then
            skip="$4"
        else
            echo "Invalid number of skip count!"
            exit 1
        fi
    fi
    if [[ -n "$5" ]]; then
        if [[ "$5" =~ ^[0-9]+$ ]]; then
            init_failures="$5"
        else
            echo "Invalid number of initial failures!"
            exit 1
        fi
    fi
    if [[ -n "$6" ]]; then
        if [[ "$6" =~ ^[0-9]+$ ]]; then
            init_silences="$6"
        else
            echo "Invalid number of initial silences!"
            exit 1
        fi
    fi
    if [[ -n "$7" ]]; then
        if [[ "$7" =~ ^0x[0-9a-f]{8}$ ]]; then
            slot_bkpt="$7"
        else
            echo "Invalid slot breakpoint!"
            exit 1
        fi
    fi

    ###########################################################################
    # Non-attacker steps
    ###########################################################################

    # Check if the ELF binary is there
    local debug_dir="$ROOT_DIR/debug/$PROJ-$1"
    local elf="$debug_dir/$1-$2.axf"
    if [[ ! -x "$elf" ]]; then
        echo "No $elf found!"
        echo "Try to compile first!"
        exit 1
    fi

    # Program the binary onto the board
    local flash_server_args=(
        "--commandline"
    )
    local flash_tool_load_args=(
        "--flash-load $elf"
        "-p MIMXRT685S"
        "-x $ROOT_DIR/scripts"
        "--bootromstall 0x50002034"
        "--args"
    )
    local flash_tool_reset_args=(
        "--reset hard"
        "-p MIMXRT685S"
        "-x $ROOT_DIR/scripts"
        "--bootromstall 0x50002034"
        "--args"
    )
    local flash_server_log=`mktemp -q`
    local flash_tool_log=`mktemp -q`
    echo "Programming $1-$2.axf onto the board ......"
    "$FLASH_SERVER" ${flash_server_args[@]} < "$FLASH_SERVER_SCRIPT" >& "$flash_server_log"
    if [[ -n `grep -i error "$flash_server_log"` ]]; then
        echo "Programming failed!"
        echo "Check $flash_server_log for details"
        exit 1
    fi
    "$FLASH_TOOL" ${flash_tool_load_args[@]} >& "$flash_tool_log"
    if (( $? != 0 )); then
        echo "Programming failed!"
        echo "Check $flash_tool_log for details"
        exit 1
    fi

    ###########################################################################
    # Attacker steps
    ###########################################################################

    # Check if arm-none-eabi-objdump or llvm-objdump is there
    local objdump=`which arm-none-eabi-objdump 2> /dev/null`
    if [[ -z "$objdump" ]]; then
        objdump=`which llvm-objdump 2> /dev/null`
        if [[ -z "$objdump" ]]; then
            echo "arm-none-eabi-objdump or llvm-objdump not found!"
            exit 1
        fi
    fi

    # Kill all screens first
    local screen_name="Randezvous-ttyACM0-$RANDOM"
    screen -S "$screen_name" -X kill >& /dev/null

    local output_dir="$DATA_DIR/$PROJ-$1"
    if [[ ! -d "$output_dir" ]]; then
        mkdir -p "$output_dir"
    fi

    readonly anchor_finish="Bye!"
    readonly anchor_fail="Error detected, rebooting"
    readonly anchor_success="Success!"
    readonly text_size=$(( 0x`"$objdump" -hw -j.text "$elf" | grep "\.text" | tr -s ' ' | cut -d' ' -f4` ))
    readonly text_addr=$(( 0x`"$objdump" -hw -j.text "$elf" | grep "\.text" | tr -s ' ' | cut -d' ' -f5` ))
    readonly data_size=$(( 0x`"$objdump" -hw -j.data "$elf" | grep "\.data" | tr -s ' ' | cut -d' ' -f4` ))
    readonly data_addr=$(( 0x`"$objdump" -hw -j.data "$elf" | grep "\.data" | tr -s ' ' | cut -d' ' -f5` ))
    readonly target_func="attacker_target"
    readonly target_size=16

    if [[ "$1" =~ ^baseline ]]; then
        readonly target_addr=$(( 0x`"$objdump" -tw -j.text "$elf" | grep "\b$target_func\b" | cut -d' ' -f1` | 1 ))
        readonly ret_addr_slot=$(( 0x20480000 - 4 ))

        echo "Resetting the board ......"
        "$FLASH_TOOL" ${flash_tool_reset_args[@]} &>> "$flash_tool_log"
        if (( $? != 0 )); then
            echo "Resetting failed!"
            echo "Check $flash_tool_log for details"
            exit 1
        fi

        local output_data="$output_dir/$1-$2.txt"
        rm -rf "$output_data"

        # Open screen to receive the output
        screen -S "$screen_name" -dm -L -fn -Logfile "$output_data" /dev/ttyACM0 115200
        screen -S "$screen_name" -X logfile flush 0

        when

        # Generate the pair of control flow target and control data slot
        echo "Feeding a pair of target and slot ......"
        screen -S "$screen_name" -X register p "$target_addr\r$ret_addr_slot\r"
        screen -S "$screen_name" -X paste p

        # Wait until the anchor shows up
        grep "$anchor_success" "$output_data" >& /dev/null
        while (( $? != 0 )); do
            sleep "$action_interval"
            grep "$anchor_success" "$output_data" >& /dev/null
        done
        screen -S "$screen_name" -X kill

        echo -e "\e[1;92mSuccess!\e[0m"
        when
        return
    fi

    # Now start automatically generating and feeding pairs
    local failures=$init_failures
    local silences=$init_silences
    for (( target = text_addr; target < text_addr + text_size - target_size; target = target + 2 )); do
        local i=`printf '0x%x' $(( target | 1 ))`
        local ii=$(( (target - text_addr) / 2 ))
        if (( skip > ii )); then
            continue
        fi

        when

        echo
        echo "Now using $i as the control flow target ($(( ii + 1 )) / $(( (text_size - target_size) / 2 )))"
        echo

        if [[ "$1" =~ ^randxom ]]; then
            ret_addr_slot=$(( 0x20480000 - 4 ))

            echo "Trying to corrupt a return address with $i"

            echo "  Resetting the board ......"
            "$FLASH_TOOL" ${flash_tool_reset_args[@]} >& "$flash_tool_log"
            if (( $? != 0 )); then
                echo "  Resetting failed!"
                echo "  Check $flash_tool_log for details"
                exit 1
            fi

            output_data="$output_dir/$1-$2-output-$i.txt"
            rm -rf "$output_data"

            # Open screen to receive the output
            screen -S "$screen_name" -dm -L -fn -Logfile "$output_data" /dev/ttyACM0 115200
            screen -S "$screen_name" -X logfile flush 0

            # Generate the pair of control flow target and control data slot
            screen -S "$screen_name" -X register p "$(( target | 1 ))\r$ret_addr_slot\r"
            screen -S "$screen_name" -X paste p

            # Wait one interval of time for one of the anchors to show up
            grep "$anchor_finish" "$output_data" >& /dev/null ||
            grep "$anchor_fail" "$output_data" >& /dev/null ||
            grep "$anchor_success" "$output_data" >& /dev/null
            if (( $? != 0 )); then
                sleep "$action_interval"
                grep "$anchor_finish" "$output_data" >& /dev/null ||
                grep "$anchor_fail" "$output_data" >& /dev/null ||
                grep "$anchor_success" "$output_data" >& /dev/null
            fi
            screen -S "$screen_name" -X kill
            if grep "$anchor_success" "$output_data" >& /dev/null; then
                echo -e "  \e[1;92mSuccess!\e[0m"
                echo "  # of failures = $failures"
                echo "  # of silences = $silences"
                when
                return
            elif grep "$anchor_fail" "$output_data" >& /dev/null; then
                failures=$(( failures + 1 ))
                echo -e "  \e[1;5;91mFailure\e[0m"
                echo "  # of failures = $failures"
                echo "  # of silences = $silences"
            else
                silences=$(( silences + 1 ))
                echo "  Nothing happened"
                echo "  # of failures = $failures"
                echo "  # of silences = $silences"
            fi
            continue
        fi

        for (( slot = data_addr; slot < data_addr + data_size; slot = slot + 4 )); do
            local j=`printf '0x%x' $slot`
            local jj=$(( (slot - data_addr) / 4 ))
            (( skip == ii )) && (( j < slot_bkpt )) && continue

            echo "Trying a pair of target and slot ($i, $j) ......"

            echo "  Resetting the board ......"
            "$FLASH_TOOL" ${flash_tool_reset_args[@]} >& "$flash_tool_log"
            if (( $? != 0 )); then
                echo "  Resetting failed!"
                echo "  Check $flash_tool_log for details"
                exit 1
            fi

            output_data="$output_dir/$1-$2-output-$i-$j.txt"
            rm -rf "$output_data"

            # Open screen to receive the output
            screen -S "$screen_name" -dm -L -fn -Logfile "$output_data" /dev/ttyACM0 115200
            screen -S "$screen_name" -X logfile flush 0

            # Generate the pair of control flow target and control data slot
            screen -S "$screen_name" -X register p "$(( target | 1 ))\r"
            screen -S "$screen_name" -X paste p
            sleep "$action_interval"
            screen -S "$screen_name" -X register p "$slot\r"
            screen -S "$screen_name" -X paste p

            # Wait one interval of time for one of the anchors to show up
            grep "$anchor_finish" "$output_data" >& /dev/null ||
            grep "$anchor_fail" "$output_data" >& /dev/null ||
            grep "$anchor_success" "$output_data" >& /dev/null
            if (( $? != 0 )); then
                sleep "$action_interval"
                grep "$anchor_finish" "$output_data" >& /dev/null ||
                grep "$anchor_fail" "$output_data" >& /dev/null ||
                grep "$anchor_success" "$output_data" >& /dev/null
            fi
            screen -S "$screen_name" -X kill
            if grep "$anchor_success" "$output_data" >& /dev/null; then
                echo -e "  \e[1;92mSuccess!\e[0m"
                echo "  # of failures = $failures"
                echo "  # of silences = $silences"
                when
                return
            elif grep "$anchor_fail" "$output_data" >& /dev/null; then
                failures=$(( failures + 1 ))
                echo -e "  \e[1;5;91mFailure\e[0m"
                echo "  # of failures = $failures"
                echo "  # of silences = $silences"
            else
                silences=$(( silences + 1 ))
                echo "  Nothing happened"
                echo "  # of failures = $failures"
                echo "  # of silences = $silences"
            fi
        done
    done
}

#
# Print out the current date/time.
#
when() {
    echo "Now is `date`"
}

#
# Entrance of the script.
#
case $1 in
"debug" )
    debug $2 $3
    ;;
"run" )
    if (( $# == 2 )); then
        for program in ${PROGRAMS[@]}; do
            run $2 $program
        done
    else
        run $2 $3
    fi
    ;;
* )
    if (( $# == 1 )); then
        # Compile each benchmark program
        for program in ${PROGRAMS[@]}; do
            compile $1 $program
        done

        echo Done
    else
        compile $1 $2
    fi
    ;;
esac
