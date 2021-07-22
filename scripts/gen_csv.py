#!/usr/bin/env python3

import argparse
import csv
import glob
import json
import os
import re
import statistics
import sys


#
# Path to the root directory of whole project.
#
root = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')

#
# Path to the debug directory where we put generated binaries.
#
debug_dir = root + '/debug'

#
# Path to the experiment data directory.
#
data_dir = root + '/data'

#
# List of configurations.
#
configurations = [
    'baseline',
    'baseline-sram',
    'randezvous',
    'randezvous-sram',
]

#
# List of benchmark suites.
#
benchmarks = [
    'beebs',
    'coremark-pro',
    'mbedtls-benchmark',
]

###############################################################################

#
# Write extracted data to an output file.
#
# @data: the data collection.
# @output: path to the output CSV file.
#
def write_data(data, output):
    with open(output, mode='w') as csv_file:
        writer = csv.writer(csv_file)

        # Do we have any program that use average + stdev?
        has_stdev = False
        for prog in data:
            for conf in data[prog]:
                if isinstance(data[prog][conf], list):
                    has_stdev = True

        # Construct and write the header row
        row = ['#Program']
        for conf in configurations:
            row.append(conf)
            if has_stdev:
                row.append('stdev')
        writer.writerow(row)

        # Construct and write a row for each program
        for prog in data:
            row = [prog]
            for conf in configurations:
                if conf in data[prog]:
                    if isinstance(data[prog][conf], list):
                        row.extend(data[prog][conf])
                    elif has_stdev:
                        row.extend([data[prog][conf], '0'])
                    else:
                        row.append(data[prog][conf])
                elif has_stdev:
                    row.extend(['', ''])
                else:
                    row.append('')
            writer.writerow(row)


#
# Generate a code size CSV file for a specified benchmark suite, assuming
# @debug_dir already contains statistics of all the generate binaries.
#
# @benchmark: name of the benchmark suite.
# @output: path to the output CSV file.
#
def gen_csv_mem(benchmark, output):
    data = {}
    for conf in configurations:
        new_debug_dir = debug_dir + '/' + benchmark + '-' + conf
        for f in sorted(glob.glob(new_debug_dir + '/*.json')):
            prog = os.path.splitext(os.path.basename(f))[0]
            stats = json.load(open(f))

            if prog not in data:
                data[prog] = {}
            data[prog][conf] = str(stats['arm-randezvous-cdla.XformedCodeSize'])

    # Write data to CSV
    write_data(data, output)


#
# Generate a performance CSV file for a specified benchmark suite, assuming
# @data_dir already contains all the experiment data needed.
#
# @benchmark: name of the benchmark suite.
# @output: path to the output CSV file.
#
def gen_csv_perf(benchmark, output):
    data = {}
    mbedtls_bench_thruput_re = re.compile('^\s*(.+?)\s*:\s*(\d+\.\d+)\s+(\w+/s)')
    mbedtls_bench_latency_re = re.compile('^\s*(.+?)\s*:.+?(\d+\.\d+)\s+(cycles/byte)')
    for conf in configurations:
        new_data_dir = data_dir + '/' + benchmark + '-' + conf

        # Process single-number data as is
        for f in sorted(glob.glob(new_data_dir + '/*.stat')):
            prog = os.path.splitext(os.path.basename(f))[0]
            number = None
            for line in open(f):
                thruput_match = mbedtls_bench_thruput_re.match(line)
                latency_match = mbedtls_bench_latency_re.match(line)
                # BEEBS
                if 'Finished' in line:
                    number = str(int(line.split(' ')[2].lstrip()))
                    break
                # CoreMark-Pro
                elif 'time(ns)' in line:
                    number = str(int(line.split('=')[-1].lstrip()))
                    break
                # MbedTLS-Benchmark
                elif thruput_match or latency_match:
                    if thruput_match:
                        alg = thruput_match.group(1)
                        unit = thruput_match.group(3)
                        prog = alg + ' (' + unit + ')'
                        if prog not in data:
                            data[prog] = {}
                        data[prog][conf] = thruput_match.group(2)
                    if latency_match:
                        alg = latency_match.group(1)
                        unit = latency_match.group(3)
                        prog = alg + ' (' + unit + ')'
                        if prog not in data:
                            data[prog] = {}
                        data[prog][conf] = latency_match.group(2)

            if number is not None:
                if prog not in data:
                    data[prog] = {}
                data[prog][conf] = number

        # Process multi-number data as average and stdev
        for f in sorted(glob.glob(new_data_dir + '/*-stat')):
            prog = os.path.splitext(os.path.basename(f))[0]
            number = None
            for line in open(f):
                thruput_match = mbedtls_bench_thruput_re.match(line)
                latency_match = mbedtls_bench_latency_re.match(line)
                # BEEBS
                if 'Finished' in line:
                    number = int(line.split(' ')[2].lstrip())
                    break
                # CoreMark-Pro
                elif 'time(ns)' in line:
                    number = int(line.split('=')[-1].lstrip())
                    break
                # MbedTLS-Benchmark
                elif thruput_match or latency_match:
                    if thruput_match:
                        alg = thruput_match.group(1)
                        unit = thruput_match.group(3)
                        prog = alg + ' (' + unit + ')'
                        if prog not in data:
                            data[prog] = {}
                        if conf not in data[prog]:
                            data[prog][conf] = []
                        data[prog][conf].append(float(thruput_match.group(2)))
                    if latency_match:
                        alg = thruput_match.group(1)
                        unit = thruput_match.group(3)
                        prog = alg + ' (' + unit + ')'
                        if prog not in data:
                            data[prog] = {}
                        if conf not in data[prog]:
                            data[prog][conf] = []
                        data[prog][conf].append(float(latency_match.group(2)))

            if number is not None:
                if prog not in data:
                    data[prog] = {}
                if conf not in data[prog]:
                    data[prog][conf] = []
                data[prog][conf].append(number)
        for prog in data:
            if conf in data[prog] and isinstance(data[prog][conf], list):
                average = float(sum(data[prog][conf])) / len(data[prog][conf])
                stdev = statistics.stdev(data[prog][conf])
                data[prog][conf] = ['{:.3f}'.format(average), '{:.3f}'.format(stdev)]

    # Write data to CSV
    write_data(data, output)


#
# The main function.
#
def main():
    # Construct a CLI argument parser
    parser = argparse.ArgumentParser(description='Generate CSV files.')
    parser.add_argument('-b', '--benchmark', choices=benchmarks,
                        default='beebs', metavar='BENCH',
                        help='Name of the benchmark suite')
    parser.add_argument('-t', '--type', choices=['mem', 'perf'],
                        default='perf', metavar='TYPE',
                        help='Type of the CSV file to generate')
    parser.add_argument('-o', '--output', metavar='FILE',
                        help='Path to the output CSV file')

    # Parse CLI arguments
    args = parser.parse_args()
    benchmark = args.benchmark
    typ = args.type
    output = typ + '-' + benchmark + '.csv'
    if args.output is not None:
        output = args.output

    # Generate CSV
    if typ == 'perf':
        gen_csv_perf(benchmark, output)
    else:
        gen_csv_mem(benchmark, output)


#
# entrance of this script.
#
if __name__ == '__main__':
    main()
