#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`
DATA_DIR="$ROOT_DIR/data"

FLASH_SERVER_SCRIPT="$ROOT_DIR/scripts/redlink-server-script"

#
# Find where the IDE is installed from some predetermined paths and export
# environment variables that point to tools in the IDE.
#
find_ide() {
    local ide_search_paths=(
        "$HOME/mcuxpresso-ide"
        "/usr/local/mcuxpresso-ide"
        "/opt/mcuxpresso-ide"
    )
    local ide_name="mcuxpressoide"
    local flash_server_name="redlinkserv"
    local flash_tool_name="crt_emu_cm_redlink"

    for path in ${ide_search_paths[@]}; do
        # Find the MCUXpresso IDE binary executable
        if [[ -x "$path/ide/$ide_name" ]]; then
            # Found it, now find a script that sets up PATH for tools in the IDE
            if [[ -f "$path/MCUXpressoPath.sh" ]]; then
                # Found it, now source the script and test if the tools we need
                # are in the PATH
                . "$path/MCUXpressoPath.sh" >& /dev/null
                local flash_server=`which $flash_server_name 2> /dev/null`
                local flash_tool=`which $flash_tool_name 2> /dev/null`
                if [[ -n "$flash_server" ]] && [[ -n "$flash_tool" ]]; then
                    # Great, now set up environment variables that point to
                    # these tools and return
                    export ECLIPSE="$path/ide/$ide_name"
                    export FLASH_SERVER="$flash_server_name"
                    export FLASH_TOOL="$flash_tool_name"
                    return
                fi
            fi
        fi
    done

    # IDE not found, exit
    echo "MCUXpresso IDE cannot be found!"
    exit 1
}

#
# Print out the usage of the script.
#
usage() {
    echo
    echo "Usage: $0 <conf> [<prog>]"
    echo
    echo "Compile a program <prog> under the configuration <conf>.  If <prog> "
    echo "is not given, all programs will be compiled."
    echo
    if type -t run > /dev/null; then
        echo "Or: $0 run <conf> [<prog>]"
        echo
        echo "Run a program <prog> under the configuration <conf>.  If <prog> "
        echo "is not given, all programs will be run."
        echo
    fi
    if type -t debug > /dev/null; then
        echo "Or: $0 debug <conf> <prog>"
        echo
        echo "Debug a program <prog> under the configuration <conf>."
        echo
    fi
}

#
# Compile a program.
#
# $1: the configuration.
# $2: the program to compile.
#
compile() {
    # Find IDE if we have not done so
    if [[ -z "$ECLIPSE" ]]; then
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
        usage
        exit 1
    fi

    # Check if the program name is valid
    if [[ ! " ${PROGRAMS[@]} " =~ " $2 " ]]; then
        echo "Program must be one of the following:"
        echo "${PROGRAMS[@]}"
        usage
        exit 1
    fi

    # Updated the .cproject file
    if [[ ! -e "$PROJ_DIR/.cproject_$1_$2" ]]; then
        echo "No .cproject_$1_$2 found in $PROJ_DIR!"
        echo "Generate one by:"
        echo
        echo "cd '$PROJ_DIR'; ./gen_cproject.py;"
        exit 1
    fi
    (cd "$PROJ_DIR"; ln -sf ".cproject_$1_$2" .cproject;)

    # Make a debug directory
    local debug_dir="$ROOT_DIR/debug/$PROJ-$1"
    if [[ ! -d "$debug_dir" ]]; then
        mkdir -p "$debug_dir"
    fi

    local elf="$PROJ_DIR/$1-$2/$1-$2.axf"
    local lib="$PROJ_DIR/$1-$2/lib$2.a"
    local stats="$PROJ_DIR/$1-$2/$1-$2.json"
    rm -rf "$elf" "$lib" "$stats"

    # Do compile
    local eclipse_args=(
        "-nosplash"
        "--launcher.suppressErrors"
        "-application org.eclipse.cdt.managedbuilder.core.headlessbuild"
        "-data $ROOT_DIR/workspace"
        "-no-indexer"
        "-cleanBuild"
    )
    echo "Compiling $2 for $1 ......"
    "$ECLIPSE" ${eclipse_args[@]} $PROJ/$1-$2 >& "$debug_dir/build-$1-$2.log"
    if [[ ! -x "$elf" ]] && [[ ! -f "$lib" ]]; then
        # Try again; the IDE sometimes may fail for no reason, but it's
        # unlikely to happen twice in a row
        "$ECLIPSE" ${eclipse_args[@]} $PROJ/$1-$2 >& "$debug_dir/build-$1-$2.log"
        if [[ ! -x "$elf" ]] && [[ ! -f "$lib" ]]; then
            echo "Compiling $2 failed!"
            echo "Check $debug_dir/build-$1-$2.log for details"
            exit 1
        fi
    fi

    # Remove the .cproject file
    (cd "$PROJ_DIR" && rm -rf .cproject;)

    # Copy the generated ELF binary to the debug directory
    if [[ -x "$elf" ]]; then
        echo "Copying $1-$2.axf to debug/$PROJ-$1 ......"
        cp "$elf" "$debug_dir"
    else
        echo "Copying lib$2.a to debug/$PROJ-$1 ......"
        cp "$lib" "$debug_dir"
    fi

    # Copy the statistics file to the debug directory
    if [[ -f "$stats" ]]; then
        echo "Copying $1-$2.json to debug/$PROJ-$1 ......"
        cp "$stats" "$debug_dir"
    fi

    echo "Done compiling $2 for $1"
    echo
}

#
# Run an already compiled benchmark program.
#
# $1: the configuration to use.
# $2: the program to run.
# $3: a string to grep for checking if the program has finished executing.
# $4: a file containing input to the program (default none).
# $5: number of seconds between two feeds of an input character (default 0.1).
# $6: number of iterations to run (default 1).
#
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

    # Check if the feed interval is a good number
    local feed_interval=0.1
    if [[ -n "$5" ]]; then
        if [[ "$5" =~ ^([0-9]+\.?[0-9]+|[0-9]*\.[0-9]+)$ ]]; then
            feed_interval="$5"
        else
            echo "Invalid number of feed interval!"
            exit 1
        fi
    fi


    # Check if the number of iterations is actually a number
    local iters=1
    if [[ -n "$6" ]]; then
        if [[ "$6" =~ ^[0-9]+$ ]]; then
            iters="$6"
        else
            echo "Number of iterations must be an integer!"
            exit 1
        fi
    fi


    # Check if the ELF binary is there
    local debug_dir="$ROOT_DIR/debug/$PROJ-$1"
    local elf="$debug_dir/$1-$2.axf"
    if [[ ! -x "$elf" ]]; then
        echo "No $elf found!"
        echo "Try to compile first!"
        exit 1
    fi

    for iter in `seq 0 $(( iters - 1 ))`; do
        # Kill all screens first
        local screen_name="Randezvous-ttyACM0"
        screen -S "$screen_name" -X kill >& /dev/null

        local perf_dir="$DATA_DIR/$PROJ-$1"
        if [[ ! -d "$perf_dir" ]]; then
            mkdir -p "$perf_dir"
        fi

        local perf_data="$perf_dir/$1-$2.stat"
        if (( $iters != 1 )); then
            perf_data="$perf_dir/$1-$2.$iter-stat"
        fi
        rm -rf "$perf_data"

        # Open screen to receive the output
        screen -S "$screen_name" -dm -L -fn -Logfile "$perf_data" /dev/ttyACM0 115200
        screen -S "$screen_name" -X logfile flush 0

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
        echo "Resetting the board ......"
        "$FLASH_TOOL" ${flash_tool_reset_args[@]} &>> "$flash_tool_log"
        if (( $? != 0 )); then
            echo "Resetting failed!"
            echo "Check $flash_tool_log for details"
            exit 1
        fi

        echo "Running $PROJ-$1/$2 ......"
        sleep 2

        # Feed input to the serial port
        if [[ -n "$4" ]] && [[ -f "$4" ]]; then
            while IFS= read -r -n1 char; do
                screen -S "$screen_name" -X register p "$char"
                screen -S "$screen_name" -X paste p
                sleep "$feed_interval"
            done < "$4"
        fi

        grep "$3" "$perf_data" >& /dev/null
        while (( $? != 0 )); do
            sleep 1
            grep "$3" "$perf_data" >& /dev/null
        done
        sleep 1
        screen -S "$screen_name" -X kill

        # Print out the result
        echo "Result:"
        echo "============================================================="
        cat "$perf_data"
        echo
    done
}

#
# Debug an already compiled benchmark program.
#
# $1: the configuration to use.
# $2: the program to run.
#
debug() {
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

    # Check if the ELF binary is there
    local debug_dir="$ROOT_DIR/debug/$PROJ-$1"
    local elf="$debug_dir/$1-$2.axf"
    if [[ ! -x "$elf" ]]; then
        echo "No $elf found!"
        echo "Try to compile first!"
        exit 1
    fi

    # Check if gdb-multiarch or arm-none-eabi-gdb is there
    local gdb=`which gdb-multiarch 2> /dev/null`
    if [[ -z "$gdb" ]]; then
        gdb=`which arm-none-eabi-gdb 2> /dev/null`
        if [[ -z "$gdb" ]]; then
            echo "gdb-multiarch or arm-none-eabi-gdb not found!"
            exit 1
        fi
    fi

    # Establish a flash server
    local flash_server_args=(
        "--commandline"
    )
    local flash_server_log=`mktemp -q`
    echo "Starting flash server ......"
    "$FLASH_SERVER" ${flash_server_args[@]} < "$FLASH_SERVER_SCRIPT" >& "$flash_server_log"
    if [[ -n `grep -i error "$flash_server_log"` ]]; then
        echo "Starting flash server failed!"
        echo "Check $flash_server_log for details"
        exit 1
    fi

    # Construct a GDB command file on the fly
    local flash_tool_args=(
        "-g"
        "-mi"
        "-p MIMXRT685S"
        "-x '$ROOT_DIR/scripts'"
        "--bootromstall 0x50002034"
        "--reset="
        "-probehandle=1"
        "-coreindex=0"
        "-cache=disable"
    )
    local flash_tool_args_all="${flash_tool_args[@]}"
    local flash_tool_log=`mktemp -q`
    local gdb_commands=(
        "set breakpoint pending on"
        "set detach-on-fork on"
        "set python print-stack none"
        "set print object on"
        "set print sevenbit-strings on"
        "set host-charset UTF-8"
        "set target-charset UTF-8"
        "set target-wide-charset UTF-32"
        "set dprintf-style call"
        "set target-async on"
        "set record full stop-at-limit off"
        "set non-stop on"
        "set auto-solib-add on"
        "set pagination off"
        "set mi-async"
        "set remotetimeout 60000"
        "target extended-remote | '$FLASH_TOOL' $flash_tool_args_all 2> '$flash_tool_log'"
        "set mem inaccessible-by-default off"
        "mon ondisconnect cont"
        "set arm force-mode thumb"
        "set remote hardware-breakpoint-limit 8"
        "mon semihost enable"
        "load '$elf'"
        "symbol-file '$elf'"
    )
    local gdb_commands_file=`mktemp -q`
    for cmd in "${gdb_commands[@]}"; do
        echo "$cmd" >> "$gdb_commands_file"
    done

    # Run GDB
    echo "Starting GDB ......"
    "$gdb" -x "$gdb_commands_file"
}
