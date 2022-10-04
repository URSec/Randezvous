#!/bin/sh

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

#
# Path to the project root directory.
#
ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

#
# Path to the LLVM source directory.
#
LLVM_SRC="$ROOT_DIR/llvm-project"

#
# Path to the LLVM build directory.
#
LLVM_BUILD="$ROOT_DIR/build/llvm"

#
# Path to the LLVM install directory.
#
LLVM_INSTALL="$ROOT_DIR/build/llvm/install"

###############################################################################

set -e

mkdir -p "$LLVM_BUILD" && cd "$LLVM_BUILD"

rm -rf CMakeCache.txt

export CC=clang
export CXX=clang++
export LD=clang
export AR=llvm-ar
export NM=llvm-nm
export RANLIB=llvm-ranlib
export READELF=llvm-readelf
export STRIP=llvm-strip

cmake -G Ninja                                                              \
      -DCMAKE_BUILD_TYPE=MinSizeRel                                         \
      -DCMAKE_INSTALL_PREFIX="$LLVM_INSTALL"                                \
      -DCMAKE_CXX_STANDARD=17                                               \
      -DLLVM_ENABLE_PROJECTS="clang;lld"                                    \
      -DLLVM_TARGETS_TO_BUILD="ARM"                                         \
      -DLLVM_ENABLE_ASSERTIONS=ON                                           \
      -DLLVM_OPTIMIZED_TABLEGEN=ON                                          \
      -DLLVM_APPEND_VC_REV=OFF                                              \
      -DLLVM_LINK_LLVM_DYLIB=ON                                             \
      -DLLVM_ENABLE_Z3_SOLVER=OFF                                           \
      "$LLVM_SRC/llvm"

# Build all
ninja

# Install only the necessary
ninja install-clang-stripped                                                \
      install-lld-stripped                                                  \
      install-LLVM-stripped                                                 \
      install-clang-cpp-stripped                                            \
      install-clang-resource-headers-stripped
