#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=tests
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "test1"
)

CONFIGURATIONS=(
    "baseline"
)

#
# Load common components.
#
. "$ROOT_DIR/scripts/common.sh"

#
# Entrance of the script.
#
case $1 in
"run" )
    if (( $# == 2 )); then
        for program in ${PROGRAMS[@]}; do
            run $2 $program "Done:"
        done
    else
        run $2 $3 "Done:"
    fi
    ;;
* )
    if (( $# == 1 )); then
        # Compile each test program
        for program in ${PROGRAMS[@]}; do
            compile $1 $program
        done

        echo Done
    else
        compile $1 $2
    fi
    ;;
esac
