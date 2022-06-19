#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=coremark-pro
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "cjpeg-rose7-preset"
    "core"
    "linear_alg-mid-100x100-sp"
    "loops-all-mid-10k-sp"
    "nnet_test"
    "parser-125k"
    "radix2-big-64k"
    "sha-test"
    "zip-test"
)

CONFIGURATIONS=(
    "baseline"
    "randezvous"
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
            run $2 $program "Bye!"
        done
    else
        run $2 $3 "Bye!"
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
