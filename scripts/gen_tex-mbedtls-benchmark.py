#!/usr/bin/env python3

import argparse
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
    'baseline-sram',
    'randezvous-sram',
]
baseline_conf = 'baseline-sram'

#
# Dict of benchmark suites and their formal names.
#
benchmarks = {
    'mbedtls-benchmark': 'MbedTLS-Benchmark',
}

###############################################################################

#
# Write the LaTeX header of the generated table to an output file.
#
# @f: a file object of the opened output file.
# @benchmark: name of the benchmark suite.
# @typ: 'latency' or 'thruput'.
# @has_stdev: whether the data has standard deviations.
# @ieee: whether to generate an IEEE-style table.
#
def write_tex_header(f, benchmark, typ, has_stdev, ieee):
    ncols = 2 if typ == 'latency' else 3

    # Synthesize a table caption
    caption = ''
    if typ == 'latency':
        caption += 'Latency'
    else:
        caption += 'Throughput'
    caption += ' of ' + benchmarks[benchmark]

    # Write a comment
    f.write('%\n% ' + caption + '.\n%\n')

    # Write \begin{table}
    if ncols < 3:
        f.write('\\begin{table}[ptb]\n')
    else:
        f.write('\\begin{table*}[ptb]\n')
    if ieee:
        # Write caption and label
        f.write('\\caption{' + caption + '}\n')
        f.write('\\label{tbl:' + typ + '-' + benchmark + '}\n')
    # Write \centering
    f.write('\\centering\n')
    # Write \sffamily
    f.write('\\sffamily\n')
    # Write \footnotesize{
    f.write('\\footnotesize{\n')
    # Restrict everything within column width
    f.write('\\resizebox{\\linewidth}{!}{\n')
    # Write \begin{tabular}
    pat = 'l' + ''.join(['rr' if has_stdev else 'r' for c in configurations])
    line = '\\begin{tabular}{@{}' + pat
    for i in range(1, ncols):
        line += '|' + pat
    line += '@{}}\n'
    f.write(line)
    # Write \toprule
    f.write('\\toprule\n')
    # Write 1st row of table header
    pat = ''.join([' & {\\bf ' + c + '} & {\\bf Stdev}' if has_stdev else ' & {\\bf ' + c + '}' for c in configurations])
    line = ' ' + pat
    for i in range(1, ncols):
        line += ' &' + pat
    line += ' \\\\\n'
    f.write(line)
    # Write 2nd row of table header
    if typ == 'latency':
        pat = ''
        for c in configurations:
            if c == baseline_conf:
                pat += ' & {(cycle/byte)}'
            else:
                pat += ' & {($\\times$)}'
            if has_stdev:
                pat += ' &'
        line = ' ' + pat
        for i in range(1, ncols):
            line += ' &' + pat
        line += ' \\\\\n'
    else:
        pat = ''
        for c in configurations:
            if c == baseline_conf:
                pat += ' &'
            else:
                pat += ' & {($\\times$)}'
            if has_stdev:
                pat += ' &'
        line = ' ' + pat
        for i in range(1, ncols):
            line += ' &' + pat
        line += ' \\\\\n'
    f.write(line)
    # Write \midrule
    f.write('\\midrule\n')


#
# Write the LaTeX footer of the generated table to an output file.
#
# @f: a file object of the opened output file.
# @benchmark: name of the benchmark suite.
# @typ: 'latency' or 'thruput'.
# @has_stdev: whether the data has standard deviations.
# @ieee: whether to generate an IEEE-style table.
#
def write_tex_footer(f, benchmark, typ, has_stdev, ieee):
    ncols = 2 if typ == 'latency' else 3

    # Synthesize a table caption
    caption = ''
    if typ == 'latency':
        caption += 'Latency'
    else:
        caption += 'Throughput'
    caption += ' Overhead on ' + benchmarks[benchmark]

    # Write \bottomrule
    f.write('\\bottomrule\n')
    # Write \end{tabular}
    f.write('\\end{tabular}\n')
    # Write end of \footnotesize{
    f.write('}}\n')
    if not ieee:
        # Write caption and label
        f.write('\\caption{' + caption + '}\n')
        f.write('\\label{tbl:' + typ + '-' + benchmark + '}\n')
    # Write \end{table}
    if ncols < 3:
        f.write('\\end{table}\n')
    else:
        f.write('\\end{table*}\n')


#
# Write the LaTeX content of the generated table to an output file.
#
# @f: a file object of the opened output file.
# @benchmark: name of the benchmark suite.
# @typ: 'latency' or 'thruput'.
# @has_stdev: whether the data has standard deviations.
# @data: the data collection.
#
def write_tex_content(f, benchmark, typ, has_stdev, data):
    ncols = 2 if typ == 'latency' else 3

    # Partition programs into N columns
    cols = []
    npercol = int((len(data) + ncols - 1) / ncols)
    for i in range(0, ncols - 1):
        cols.append(list(data.keys())[i*npercol:(i+1)*npercol])
    cols.append(list(data.keys())[(ncols-1)*npercol:])

    # Write each row and collect statistics in the meantime
    stats = dict.fromkeys([c for c in configurations if c != baseline_conf], [])
    for i in range(0, npercol):
        line = ' '
        for j in range(0, ncols):
            if j != 0:
                line += ' &'
            if i < len(cols[j]):
                prog = cols[j][i]
                line += ' ' + prog.replace('_', '\\_')
                for conf in configurations:
                    if isinstance(data[prog][conf], list):
                        number = data[prog][conf][0]
                    else:
                        number = data[prog][conf]
                    if conf == baseline_conf:
                        if isinstance(number, int):
                            # Generate comma-separated numbers for baseline
                            number = '{:,}'.format(int(number))
                    else:
                        if isinstance(data[prog][baseline_conf], list):
                            baseline = float(data[prog][baseline_conf][0])
                        else:
                            baseline = float(data[prog][baseline_conf])
                        number = float(number) / baseline
                        stats[conf].append(number)
                        number = '{0:.3f}'.format(number)
                    line += ' & ' + number
                    if has_stdev:
                        if isinstance(data[prog][conf], list):
                            number = data[prog][conf][1]
                        else:
                            number = 0
                        if conf == baseline_conf:
                            number = '{0:.2f}'.format(float(number))
                        else:
                            if isinstance(data[prog][baseline_conf], list):
                                baseline = float(data[prog][baseline_conf][0])
                            else:
                                baseline = float(data[prog][baseline_conf])
                            number = '{0:.3f}'.format(float(number) / baseline)
                        line += ' & ' + number
            else:
                for conf in configurations:
                    line += ' &'
                    if has_stdev:
                        line += ' &'

        line += ' \\\\\n'
        f.write(line)

    # Write \midrule
    f.write('\\midrule\n')

    # Write statistic summaries: Min
    multicols = (len(configurations) * (2 if has_stdev else 1) + 1) * ncols - 2
    f.write('  {\\bf Min ($\\times$)} & \\multicolumn{' + str(multicols) + '}{r}{}')
    for conf in stats:
        f.write(' & ' + "{0:.3f}".format(min(stats[conf])))
    f.write(' \\\\\n')
    # Write statistic summaries: Max
    f.write('  {\\bf Max ($\\times$)} & \\multicolumn{' + str(multicols) + '}{r}{}')
    for conf in stats:
        f.write(' & ' + "{0:.3f}".format(max(stats[conf])))
    f.write(' \\\\\n')
    # Write statistic summaries: Geomean
    f.write('  {\\bf Geomean ($\\times$)} & \\multicolumn{' + str(multicols) + '}{r}{}')
    for conf in stats:
        f.write(' & ' + "{0:.3f}".format(statistics.geometric_mean(stats[conf])))
    f.write(' \\\\\n')

#
# Write extracted data to an output file.
#
# @benchmark: name of the benchmark suite.
# @typ: 'latency' or 'thruput'.
# @ieee: whether to generate an IEEE-style table.
# @data: the data collection.
# @output: path to the output LaTeX file.
#
def write_data(benchmark, typ, ieee, data, output):
    # Do we have any program that uses average + stdev?
    has_stdev = False
    for prog in data:
        for conf in data[prog]:
            if isinstance(data[prog][conf], list):
                assert len(data[prog][conf]) == 2, 'Not average + stdev list?'
                has_stdev = True

    with open(output, mode='w') as f:
        # Write header
        write_tex_header(f, benchmark, typ, has_stdev, ieee)

        # Write table content
        write_tex_content(f, benchmark, typ, has_stdev, data)

        # Write footer
        write_tex_footer(f, benchmark, typ, has_stdev, ieee)


#
# Generate a LaTeX file for a specified benchmark suite, assuming @data_dir
# already contains all the experiment data needed.
#
# @benchmark: name of the benchmark suite.
# @typ: 'latency' or 'thruput'.
# @ieee: whether to generate an IEEE-style table.
# @output: path to the output LaTeX file.
#
def gen_tex(benchmark, typ, ieee, output):
    if typ == 'latency':
        mbedtls_bench_re = re.compile('^\s*(.+?)\s*:.+?(\d+\.\d+)\s+(cycles/byte)')
    else:
        mbedtls_bench_re = re.compile('^\s*(.+?)\s*:\s*(\d+\.\d+)\s+(\w+/s)')

    data = {}
    for conf in configurations:
        new_data_dir = data_dir + '/' + benchmark + '-' + conf

        # Process single-number data as is
        for f in sorted(glob.glob(new_data_dir + '/*.stat')):
            for line in open(f):
                match = mbedtls_bench_re.match(line)
                # MbedTLS-Benchmark
                if match:
                    alg = match.group(1)
                    unit = match.group(3)
                    prog = alg + ' (' + unit + ')' if typ == 'thruput' else alg
                    if prog not in data:
                        data[prog] = {}
                    data[prog][conf] = float(match.group(2))

        # Process multi-number data as average and stdev
        for f in sorted(glob.glob(new_data_dir + '/*-stat')):
            for line in open(f):
                match = mbedtls_bench_re.match(line)
                # MbedTLS-Benchmark
                if match:
                    alg = match.group(1)
                    unit = match.group(3)
                    prog = alg + ' (' + unit + ')' if typ == 'thruput' else alg
                    if prog not in data:
                        data[prog] = {}
                    if conf not in data[prog]:
                        data[prog][conf] = []
                    data[prog][conf].append(float(match.group(2)))

        for prog in data:
            if conf in data[prog] and isinstance(data[prog][conf], list):
                average = float(sum(data[prog][conf])) / len(data[prog][conf])
                stdev = statistics.stdev(data[prog][conf])
                data[prog][conf] = [average, stdev]

    # Write data to LaTeX
    write_data(benchmark, typ, ieee, data, output)


#
# The main function.
#
def main():
    # Construct a CLI argument parser
    parser = argparse.ArgumentParser(description='Generate LaTeX files.')
    parser.add_argument('-b', '--benchmark', choices=benchmarks.keys(),
                        default='mbedtls-benchmark', metavar='BENCH',
                        help='Name of the benchmark suite')
    parser.add_argument('-t', '--type', choices=['latency', 'thruput'],
                        default='latency', metavar='TYPE',
                        help='Type of the LaTeX file to generate')
    parser.add_argument('--ieee', action='store_true',
                        help='Generate an IEEE-style table')
    parser.add_argument('-o', '--output', metavar='FILE',
                        help='Path to the output LaTeX file')

    # Parse CLI arguments
    args = parser.parse_args()
    benchmark = args.benchmark
    typ = args.type
    ieee = args.ieee
    output = typ + '-' + benchmark + '.tex'
    if args.output is not None:
        output = args.output

    # Generate LaTeX
    gen_tex(benchmark, typ, ieee, output)


#
# entrance of this script.
#
if __name__ == '__main__':
    main()
