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
# Path to the newlib source directory.
#
NEWLIB_SRC="$ROOT_DIR/newlib-cygwin"

#
# Path to the newlib build directory.
#
NEWLIB_BUILD="$ROOT_DIR/build/newlib-cygwin"

#
# Path to the newlib install directory.
#
NEWLIB_INSTALL="$ROOT_DIR/build/newlib-cygwin/install"

#
# Path to where arm-none-eabi libgcc is installed.
#
ARM_NONE_EABI_GCC_PATH=`dirname $(arm-none-eabi-gcc -print-libgcc-file-name)`

#
# Path to the LLVM build directory.
#
LLVM_BUILD="$ROOT_DIR/build/llvm"

#
# Path to the LLVM install directory.
#
LLVM_INSTALL="$ROOT_DIR/build/llvm/install"


#
# The target for which to build newlib.
#
TARGET="arm-none-eabihf"

#
# Path to the C compiler to use.
#
CC_FOR_TARGET="$LLVM_INSTALL/bin/clang"
export CC_FOR_TARGET

#
# Path to the C compiler to use.
#
GCC_FOR_TARGET="$CC_FOR_TARGET"
export GCC_FOR_TARGET

#
# Path to the C++ compiler to use.
#
CXX_FOR_TARGET="$CC_FOR_TARGET"
export CXX_FOR_TARGET

#
# Path to the assembler to use.
#
AS_FOR_TARGET="$CC_FOR_TARGET"
export AS_FOR_TARGET

#
# Path to the linker to use.
#
LD_FOR_TARGET="$CC_FOR_TARGET"
export LD_FOR_TARGET

#
# Path to the archiver to use.
#
AR_FOR_TARGET="$LLVM_BUILD/bin/llvm-ar"
export AR_FOR_TARGET

#
# Path to the NM tool.
#
NM_FOR_TARGET="$LLVM_BUILD/bin/llvm-nm"
export NM_FOR_TARGET

#
# Path to the RANLIB tool.
#
RANLIB_FOR_TARGET="$LLVM_BUILD/bin/llvm-ranlib"
export RANLIB_FOR_TARGET

#
# Path to the READELF tool.
#
READELF_FOR_TARGET="$LLVM_BUILD/bin/llvm-readelf"
export READELF_FOR_TARGET

#
# Path to the STRIP tool.
#
STRIP_FOR_TARGET="$LLVM_BUILD/bin/llvm-strip"
export STRIP_FOR_TARGET

#
# CFLAGS to use.
#
CFLAGS_FOR_TARGET="--target=$TARGET"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -mcpu=cortex-m33"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -mfpu=fpv5-sp-d16"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -mfloat-abi=hard"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -mthumb"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -g"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -Os"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -flto"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -ffunction-sections"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -fdata-sections"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -ffreestanding"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -fomit-frame-pointer"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -nostdinc"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -I$ARM_NONE_EABI_GCC_PATH/include"
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -I$ARM_NONE_EABI_GCC_PATH/include-fixed"
export CFLAGS_FOR_TARGET

#
# LDFLAGS to use.
#
LDFLAGS_FOR_TARGET="--target=$TARGET"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -mcpu=cortex-m33"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -mfpu=fpv5-sp-d16"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -mfloat-abi=hard"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -mthumb"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -g"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -Os"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -flto"
LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET -fuse-ld=lld"
export LDFLAGS_FOR_TARGET

###############################################################################

set -e

mkdir -p "$NEWLIB_BUILD" && cd "$NEWLIB_BUILD"

"$NEWLIB_SRC/configure" --target="$TARGET"                                  \
                        --srcdir="$NEWLIB_SRC"                              \
                        --prefix="$NEWLIB_INSTALL"                          \
                        --disable-newlib-supplied-syscalls                  \
                        --with-cpu=armv8m                                   \
                        --with-mode=thumb

make all-target-newlib
make install-target-newlib
