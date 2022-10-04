#!/usr/bin/env bash

# Copyright (c) 2022, University of Rochester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=pinlock
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "pinlock"
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
            run $2 $program "Bye!" "$ROOT_DIR/scripts/pinlock-input.txt" 0.1 10
        done
    else
        run $2 $3 "Bye!" "$ROOT_DIR/scripts/pinlock-input.txt" 0.1 10
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
