#!/usr/bin/env bash

# Copyright (c) 2021-2022, University of Rochester
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

PROJ=beebs
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "aha-compress"
    "aha-mont64"
    "bs"
    "bubblesort"
    "cnt"
    "compress"
    "cover"
    "crc"
    "crc32"
    "ctl-stack"
    "ctl-string"
    "ctl-vector"
    "cubic"
    "dijkstra"
    "dtoa"
    "duff"
    "edn"
    "expint"
    "fac"
    "fasta"
    "fdct"
    "fibcall"
    "fir"
    "frac"
    "huffbench"
    "insertsort"
    "janne_complex"
    "jfdctint"
    "lcdnum"
    "levenshtein"
    "ludcmp"
    "matmult-float"
    "matmult-int"
    "mergesort"
    "miniz"
    "minver"
    "nbody"
    "ndes"
    "nettle-aes"
    "nettle-arcfour"
    "nettle-cast128"
    "nettle-des"
    "nettle-md5"
    "nettle-sha256"
    "newlib-exp"
    "newlib-log"
    "newlib-mod"
    "newlib-sqrt"
    "ns"
    "nsichneu"
    "picojpeg"
    "prime"
    "qrduino"
    "qsort"
    "qurt"
    "recursion"
    "rijndael"
    "select"
    "sglib-arraybinsearch"
    "sglib-arrayheapsort"
    "sglib-arrayquicksort"
    "sglib-dllist"
    "sglib-hashtable"
    "sglib-listinsertsort"
    "sglib-listsort"
    "sglib-queue"
    "sglib-rbtree"
    "slre"
    "sqrt"
    "st"
    "statemate"
    "stb_perlin"
    "stringsearch1"
    "strstr"
    "tarai"
    "trio-snprintf"
    "trio-sscanf"
    "ud"
    "whetstone"
    "wikisort"
)

PROGRAMS_EXCLUDED=(
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
        for prog in ${PROGRAMS[@]}; do
            if [[ " ${PROGRAMS_EXCLUDED[@]} " =~ " $prog " ]]; then
                continue
            fi
            run $2 $prog "Bye!"
        done
    else
        run $2 $3 "Bye!"
    fi
    ;;
* )
    if (( $# == 1 )); then
        # Compile each benchmark program
        for prog in ${PROGRAMS[@]}; do
            if [[ " ${PROGRAMS_EXCLUDED[@]} " =~ " $prog " ]]; then
                continue
            fi
            compile $1 $prog
        done

        echo Done
    else
        compile $1 $2
    fi
    ;;
esac
