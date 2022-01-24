#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=mimxrt685s
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "mimxrt685s"
)

CONFIGURATIONS=(
    "baseline"
)

#
# Load common components.
#
. "$ROOT_DIR/scripts/common.sh"

#
# Disable the run() and debug() functions.
#
unset run
unset debug

#
# Entrance of the script.
#
if (( $# == 1 )); then
    # Compile each program
    for program in ${PROGRAMS[@]}; do
        compile $1 $program
    done

    echo Done
else
    compile $1 $2
fi
