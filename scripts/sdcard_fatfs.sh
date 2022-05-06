#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=sdcard_fatfs
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "sdcard_fatfs"
)

CONFIGURATIONS=(
    "baseline"
    "baseline-sram"
    "randezvous"
    "randezvous-sram"
)

#
# Load common components.
#
. "$ROOT_DIR/scripts/common.sh"

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
            run $2 $program "Bye!" "" 0.1 10
        done
    else
        run $2 $3 "Bye!" "" 0.1 10
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
