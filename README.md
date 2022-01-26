# The Randezvous Project

This repository contains and organizes code that we used to evaluate Randezvous.

## Brief Introduction

Randezvous is a software defense against control-flow hijacking attacks on
embedded microcontroller (MCU) systems, built up on diversification.
Unlike other control-flow hijacking defenses on MCU systems, Randezvous assumes
a broader threat model in which attackers can not only use buffer overflows to
corrupt memory but also use buffer overreads to leak memory content.
In order to mitigate such powerful attacks, Randezvous employs several novel
techniques to protect in-memory control data from leakage and corruption.
It also slows down brute force attacks to make randomization effective even
with MCUs' limited memory.

## Directory Hierarchy

```shell
Silhouette-Evaluation
|-- build                    # Directory for building LLVM, Newlib, and compiler-rt
|   |-- build.llvm.sh        # Script to build LLVM
|   |-- build.newlib.sh      # Script to build Newlib
|   |-- build.compiler.rt.sh # Script to build Newlib
|
|-- data                     # Directory containing generated experiment data (to
|                            # be created by our scripts)
|
|-- debug                    # Directory containing compiled binaries and build
|                            # logs (to be created by our scripts)
|
|-- llvm-project             # A submodule containing source code of LLVM and
|                            # Randezvous passes
|
|-- newlib-cygwin            # A submodule containing source code of Newlib
|
|-- scripts                  # Directory containing scripts
|   |-- import.sh            # Script to import projects into IDE
|   |-- hal.sh               # Script to compile HAL library for MIMXRT685-EVK
|   |-- beebs.sh             # Script to compile/run BEEBS benchmarks
|   |-- coremark-pro.sh      # Script to compile/run CoreMark-Pro benchmarks
|   |-- mbedtls-benchmark.sh # Script to compile/run MBedTLS-Benchmark
|   |-- tests.sh             # Script to compile/run test programs
|   |-- entropy.py           # Script to calculate security analysis results
|   |-- gen_csv.py           # Script to collect experiment results into CSV files
|   |-- gen_tex*.py          # Scripts to generate LaTeX tables for paper writing
|
|-- workspace                # Directory containing source code
|   |-- beebs                # Source code of BEEBS benchmarks
|   |-- coremark-pro         # Source code of CoreMark-Pro benchmarks
|   |-- mbedtls-benchmark    # Source code of MBedTLS-Benchmark
|   |-- tests                # Source code of test programs
|   |-- mimxrt685s           # Source code of HAL library for MIMXRT685-EVK
|
|-- README.md                # This README file
```

## Prerequisites

- We assume the host operating system is Linux. Other operating systems may
  work but were not tested.
- We use CMake, Ninja, and Clang to build the LLVM-based Randezvous compiler,
  so `cmake`, `ninja`, and `clang` of appropriate versions must be found in
  `PATH`.
- We use the Randezvous compiler to build Newlib and compiler-rt, so make sure
  that common development tools needed to build Newlib and compiler-rt for
  bare-metal ARM environments (such as `arm-none-eabi-gcc` and `make`) are
  there in `PATH`.  In particular, one of our build scripts uses
  `arm-none-eabi-gcc` to find out where a bare-metal ARM `libgcc` is installed.
- We use [MCUXpresso IDE](https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE)
  to build, run, and debug benchmarks and require the IDE to be installed at
  `/usr/local`, `/opt`, or `$HOME`.
- We use an NXP MIMXRT685-EVK board to run benchmarks and assume a
  readable/writable character device `/dev/ttyACM0` is connected to the board's
  serial port after plugging in the board.
- We use GNU Screen to receive program output from the board's serial port, so
  `screen` of an appropriate version must be found in `PATH`.  If you use GNU
  Screen, please avoid naming your sessions to `Randezvous-ttyACM0`; this is
  the session name we use.
- We use GDB to debug ELF binaries and have debugging support included in our
  scripts.  If you would like to use our script for debugging, make sure either
  `gdb-multiarch` or `arm-none-eabi-gdb` is there in `PATH`.

## Detailed Steps

### Set up the Environment

The following steps will set up the environment from scratch.  They only need
to be done once.

1. Download [MCUXpresso IDE](https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE)
   and install it at `/usr/local`, `/opt`, or `$HOME`.  Note that although our
   scripts build programs using the IDE in headless mode (i.e., no GUI
   required), the IDE still needs to be run in GUI for the first time in order
   for the embedded development tools that come with it to be unpacked in the
   file system.
2. Clone this repository.
   ```shell
   git clone --recurse-submodules URL
   ```
3. Build the Randezvous compiler.
   ```shell
   cd Randezvous && ./build/build.llvm.sh
   ```
   Note that all our scripts (in the `build` and `scripts` directories) are
   CWD-agnostic; each of them can be run from any working directory and would
   have the same outcome.  After `./build/build.llvm.sh` finishes, the
   Randezvous compiler will be installed in `build/llvm/install/bin`.
4. Build Newlib and compiler-rt.
   ```shell
   ./build/build.newlib.sh && ./build/build.compiler.rt.sh
   ```
   After the two scripts finish, Newlib will be installed in
   `build/newlib-cygwin/install` and compiler-rt will be installed in
   `build/compiler-rt/install`.
5. Import all the IDE projects in the `workspace` directory into the IDE.
   ```shell
   ./scripts/import.sh
   ```
6. Build a baseline version of the HAL library.  All our programs will link
   against the baseline HAL library.
   ```shell
   ./scripts/hal.sh baseline
   ```

### Build, Debug, and Run Programs

We have three scripts `beebs.sh`, `coremark-pro.sh`, and `mbedtls-benchmark.sh`
that can compile, debug, and run three benchmark suites
([BEEBS](https://beebs.mageec.org/),
[CoreMark-Pro](https://www.eembc.org/coremark-pro), and
[MbedTLS-Benchmark](https://github.com/ARMmbed/mbedtls/blob/development/programs/test/benchmark.c)),
respectively.  These scripts support identical command-line argument formats
```shell
./scripts/<script-name>.sh <CONFIG> [PROGRAM [PROGRAM]...]
```
or
```shell
./scripts/<script-name>.sh run <CONFIG> [PROGRAM [PROGRAM]...]
```
or
```shell
./scripts/<script-name>.sh debug <CONFIG> <PROGRAM>
```
where `CONFIG` is the name of a configuration (see below) and `PROGRAM` is the
name of a program in the corresponding benchmark suite.  For compile and run,
if `PROGRAM` is not specified, all the programs in the corresponding benchmark
suite will be compiled/run.  For example, running `./scripts/beebs.sh baseline`
will compile all the benchmark programs in BEEBS using the Baseline
configuration, and running `./scripts/coremark-pro.sh run randezvous zip-test`
will run the `zip-test` program in CoreMark-Pro that was compiled using the
Randezvous configuration.

More specifically, we use four configurations of experiments for each benchmark
suite:
- **Baseline**: Compile the programs without any of our passes, denoted as
  `baseline`;
- **Baseline w/ code loaded to SRAM**: The same as `baseline` except that code
  is loaded to SRAM for execution, denoted as `baseline-sram`;
- **Randezvous**: Turn on all the Randezvous passes with all seeds set to zero,
  denoted as `randezvous`;
- **Randezvous w/ code loaded to SRAM**: The same as `randezvous` except that
  code is loaded to SRAM for execution, denoted as `randezvous-sram`.

The following shell code compiles all benchmarks we use, with all possible
configurations:
```shell
for conf in baseline baseline-sram randezvous randezvous-sram; do
    ./beebs.sh $conf
    ./coremark-pro.sh $conf
    ./mbedtls-benchmark.sh $conf
done
```
Note that compilation using our scripts must be done one at a time (i.e., **no
parallel compiling of multiple programs**).  This is because the IDE runs a
singleton mode.

The following shell code runs all benchmarks compiled by the above shell code:
```shell
for conf in baseline baseline-sram randezvous randezvous-sram; do
    ./beebs.sh run $conf
    ./coremark-pro.sh run $conf
    ./mbedtls-benchmark.sh run $conf
done
```
Note that in order to run programs, an NXP MIMXRT685-EVK board must be
connected to the host machine.

### Collect Experiment Results

After compiling a benchmark program, an ELF binary with a `.axf` suffix will be
placed in the `debug` directory, and after running a program, experiment data
with performance metrics will be generated in the `data` directory.  The names
of all the subdirectories and files under `debug` and `data` are
self-explanatory.  For example, `debug/beebs-baseline/baseline-whetstone.axf`
is the ELF binary of the `whetstone` program in BEEBS compiled using the
`baseline` configuration, and
`data/coremark-pro-randezvous-sram/randezvous-sram-core.stat` contains the
execution time of running the `core` program in CoreMark-Pro compiled with the
`randezvous-sram` configuration.

You can use the `scripts/gen_csv.py` script to collect the raw experiment data
and write the summarized results to a CSV file.  This script takes three
optional command-line arguments:
```shell
-b benchmark_name # "beebs", "coremark-pro", or "mbedtls-benchmark", default "beebs"
-t data_type      # "perf", "codesize", or "datasize", default "perf"
-o output_file    # Path of the output CSV file; if not specified, a default
                  # name "data_type-benchmark_name.csv" will be used
```
For example, if you want to see the performance numbers on BEEBS, run
```shell
./scripts/gen_csv.py -b beebs -t perf
```
and you will get an output file named `perf-beebs.csv` in the working directory.
