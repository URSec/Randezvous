#!/usr/bin/env python3

import argparse
import glob
import json
import os
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
# Dict of configurations and their formal names.
#
configurations = {
    'baseline-sram': 'Baseline',
    'randezvous-sram': '{\\System}',
}
baseline_conf = 'baseline-sram'

#
# Dict of benchmark suites and their formal names.
#
benchmarks = {
    'beebs': 'BEEBS',
    'coremark-pro': 'CoreMark-Pro',
}

#
# Dict of types and their formal names.
#
types = {
    'mem': 'Memory Usage',
}

###############################################################################

#
# Write the LaTeX header of the generated table to an output file.
#
# @f: a file object of the opened output file.
# @benchmark: name of the benchmark suite.
# @typ: type of the LaTeX file to generate.
# @ieee: whether to generate an IEEE-style table.
#
def write_tex_header(f, benchmark, typ, ieee):
    ncols = 1

    # Synthesize a table caption
    caption = benchmarks[benchmark] + ' ' + types[typ]

    # Write a comment
    f.write('%\n% ' + caption + '.\n%\n')

    # Write \begin{table}
    if ncols < 3:
        f.write('\\begin{table}[tb]\n')
    else:
        f.write('\\begin{table*}[tb]\n')
    if ieee:
        # Write caption and label
        f.write('\\caption{' + caption + '}\n')
        f.write('\\label{tbl:' + typ + '-' + benchmark + '}\n')
    # Write \centering
    f.write('\\centering\n')
    # Write {\sffamily
    f.write('{\\sffamily\n')
    # Write \footnotesize{
    f.write('\\footnotesize{\n')
    # Restrict everything within column width
    f.write('\\resizebox{\\linewidth}{!}{\n')
    # Write \begin{tabular}
    line = '\\begin{tabular}{@{}'
    for i in range(0, ncols):
        if i != 0:
            line += '|'
        line += 'l'
        for c in configurations:
            line += 'rr'
    line += '@{}}\n'
    f.write(line)
    # Write \toprule
    f.write('\\toprule\n')
    # Write 1st row of table header
    line = ' '
    for i in range(0, ncols):
        if i != 0:
            line += ' &'
        for c in configurations:
            line += ' & {\\bf ' + configurations[c] + '}'
            line += ' & {\\bf ' + configurations[c] + '}'
    line += ' \\\\\n'
    f.write(line)
    # Write 2nd row of table header
    line = ' '
    for i in range(0, ncols):
        if i != 0:
            line += ' &'
        for c in configurations:
            if c == baseline_conf:
                line += ' & {\\bf Code} {(bytes)}'
                line += ' & {\\bf Data} {(bytes)}'
            else:
                line += ' & {\\bf Code} {($\\times$)}'
                line += ' & {\\bf Data} {($\\times$)}'
    line += ' \\\\\n'
    f.write(line)
    # Write \midrule
    f.write('\\midrule\n')


#
# Write the LaTeX footer of the generated table to an output file.
#
# @f: a file object of the opened output file.
# @benchmark: name of the benchmark suite.
# @typ: type of the LaTeX file to generate.
# @ieee: whether to generate an IEEE-style table.
#
def write_tex_footer(f, benchmark, typ, ieee):
    ncols = 1

    # Synthesize a table caption
    caption = benchmarks[benchmark] + ' ' + types[typ]

    # Write \bottomrule
    f.write('\\bottomrule\n')
    # Write \end{tabular}
    f.write('\\end{tabular}\n')
    # Write end of \resizebox{, \footnotesize{, and {\sffamily
    f.write('}}}\n')
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
# @typ: type of the LaTeX file to generate.
# @data: the data collection.
#
def write_tex_content(f, benchmark, typ, data):
    ncols = 1
    memtypes = ['codesize', 'datasize']

    # Partition programs into N columns
    cols = []
    npercol = int((len(data) + ncols - 1) / ncols)
    for i in range(0, ncols - 1):
        cols.append(list(data.keys())[i*npercol:(i+1)*npercol])
    cols.append(list(data.keys())[(ncols-1)*npercol:])

    # Write each row and collect statistics in the meantime
    stats = {}
    for i in range(0, npercol):
        line = ' '
        for j in range(0, ncols):
            if j != 0:
                line += ' &'
            if i < len(cols[j]):
                prog = cols[j][i]
                line += ' ' + prog.replace('_', '\\_')
                for conf in configurations:
                    for mt in memtypes:
                        number = data[prog][conf][mt]
                        if conf not in stats:
                            stats[conf] = {}
                        if mt not in stats[conf]:
                            stats[conf][mt] = []
                        if conf == baseline_conf:
                            stats[conf][mt].append(number)
                            if isinstance(number, int):
                                # Generate comma-separated numbers for baseline
                                number = '{:,}'.format(int(number))
                            else:
                                number = '{0:,.3f}'.format(float(number))
                        else:
                            baseline = float(data[prog][baseline_conf][mt])
                            number = float(number) / baseline
                            stats[conf][mt].append(number)
                            number = '{0:.3f}'.format(number)
                        line += ' & ' + number
            else:
                for conf in configurations:
                    line += ' & &'

        line += ' \\\\\n'
        f.write(line)

    # Write \midrule
    f.write('\\midrule\n')

    # Write statistic summaries: Min
    f.write('  {\\bf Min}')
    for conf in stats:
        for mt in memtypes:
            if conf == baseline_conf:
                f.write(' & ' + "{:,}".format(int(min(stats[conf][mt]))))
            else:
                f.write(' & ' + "{0:.3f}".format(min(stats[conf][mt])))
    f.write(' \\\\\n')
    # Write statistic summaries: Max
    f.write('  {\\bf Max}')
    for conf in stats:
        for mt in memtypes:
            if conf == baseline_conf:
                f.write(' & ' + "{:,}".format(int(max(stats[conf][mt]))))
            else:
                f.write(' & ' + "{0:.3f}".format(max(stats[conf][mt])))
    f.write(' \\\\\n')
    # Write statistic summaries: Geomean
    f.write('  {\\bf Geomean}')
    for conf in stats:
        for mt in memtypes:
            if conf == baseline_conf:
                f.write(' & ---')
            else:
                f.write(' & ' + "{0:.3f}".format(statistics.geometric_mean(stats[conf][mt])))
    f.write(' \\\\\n')

#
# Write extracted data to an output file.
#
# @benchmark: name of the benchmark suite.
# @typ: type of the LaTeX file to generate.
# @ieee: whether to generate an IEEE-style table.
# @data: the data collection.
# @output: path to the output LaTeX file.
#
def write_data(benchmark, typ, ieee, data, output):
    with open(output, mode='w') as f:
        # Write header
        write_tex_header(f, benchmark, typ, ieee)

        # Write table content
        write_tex_content(f, benchmark, typ, data)

        # Write footer
        write_tex_footer(f, benchmark, typ, ieee)


#
# Generate a LaTeX file for a specified benchmark suite, assuming @data_dir
# already contains all the experiment data needed.
#
# @benchmark: name of the benchmark suite.
# @typ: type of the LaTeX file to generate.
# @ieee: whether to generate an IEEE-style table.
# @output: path to the output LaTeX file.
#
def gen_tex(benchmark, typ, ieee, output):
    data = {}
    data2 = {}
    for conf in configurations:
        new_data_dir = data_dir + '/' + benchmark + '-' + conf

        # Process single-number data as is
        for f in sorted(glob.glob(new_data_dir + '/*.stat')):
            prog = os.path.splitext(os.path.basename(f))[0].split(conf + '-')[1]
            number = None
            for line in open(f):
                # BEEBS
                if 'Finished' in line:
                    number = int(line.split(' ')[2].lstrip())
                    if conf == baseline_conf:
                        if number < 500:
                            number = None
                    elif prog not in data or baseline_conf not in data[prog]:
                        number = None
                    break
                # CoreMark-Pro
                elif 'time(ns)' in line:
                    number = int(line.split('=')[-1].lstrip())
                    break

            if number is not None:
                if prog not in data:
                    data[prog] = {}
                data[prog][conf] = number

        # Process multi-number data as average and stdev
        for f in sorted(glob.glob(new_data_dir + '/*-stat')):
            prog = os.path.splitext(os.path.basename(f))[0].split(conf + '-')[1]
            number = None
            for line in open(f):
                # BEEBS
                if 'Finished' in line:
                    number = int(line.split(' ')[2].lstrip())
                    break
                # CoreMark-Pro
                elif 'time(ns)' in line:
                    number = int(line.split('=')[-1].lstrip())
                    break

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
                data[prog][conf] = [average, stdev]

    if typ == 'mem':
        codesize_key = 'arm-randezvous-cdla.XformedCodeSize'
        datasize_keys = [
            'arm-randezvous-gdlr.NumBytesInRodata',
            'arm-randezvous-gdlr.NumBytesInData',
            'arm-randezvous-gdlr.NumBytesInBss',
        ]

        for conf in configurations:
            new_debug_dir = debug_dir + '/' + benchmark + '-' + conf
            for f in sorted(glob.glob(new_debug_dir + '/*.json')):
                prog = os.path.splitext(os.path.basename(f))[0].split(conf + '-')[1]

                if prog not in data:
                    continue
                if prog not in data2:
                    data2[prog] = {}
                if conf not in data2[prog]:
                    data2[prog][conf] = {}

                stats = json.load(open(f))

                codesize = stats[codesize_key]
                datasize = 0
                for key in datasize_keys:
                    if key in stats:
                        datasize += stats[key]

                data2[prog][conf]['codesize'] = codesize
                data2[prog][conf]['datasize'] = datasize
        data = data2

    # Write data to LaTeX
    write_data(benchmark, typ, ieee, data, output)


#
# The main function.
#
def main():
    # Construct a CLI argument parser
    parser = argparse.ArgumentParser(description='Generate LaTeX files.')
    parser.add_argument('-b', '--benchmark', choices=benchmarks.keys(),
                        default=list(benchmarks.keys())[0], metavar='BENCH',
                        help='Name of the benchmark suite')
    parser.add_argument('-t', '--type', choices=types.keys(),
                        default=list(types.keys())[0], metavar='TYPE',
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
