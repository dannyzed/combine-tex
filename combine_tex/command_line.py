import argparse
import re
import os
import shutil

numFiguresProcessed = 0


def parse_line(line):
    m = re.search('input\{([^\}]*)', line)
    if m:
        return m.group(1)
    else:
        return []


def parse_for_figure(line):
    m = re.search('\{(\S*\/([^\/]*\.pdf))\}', line)
    if m:
        return m.group(1), m.group(2)
    else:
        return [], []


def remake_figure_line(line):
    global numFiguresProcessed
    numFiguresProcessed += 1
    fig_name = 'f'
    if numFiguresProcessed < 10:
        fig_name += '0' + str(numFiguresProcessed)
    else:
        fig_name += str(numFiguresProcessed)
    fig_name += '.pdf'
    # return re.sub(r'\{(\S*\/([^\/]*\.pdf))\}', r'{\2}', line)
    return re.sub(r'\{(\S*\/([^\/]*\.pdf))\}', '{' + fig_name + '}', line), fig_name


def find_file_depends(filename):
    infile = open(filename)
    file_list = []
    for line in infile:
        depending_file = parse_line(line)
        if depending_file:
            file_list.append(depending_file)
            more_files = find_file_depends(depending_file)
            if more_files:
                file_list.append(more_files)
    return file_list


def remake_file(file_name, out_folder):
    infile = open(file_name)
    outfile = open(out_folder + '/' + file_name, 'w+')
    for line in infile:
        figure_path, fig_name = parse_for_figure(line)
        if figure_path:
            line, fig_name = remake_figure_line(line)
            shutil.copy2(figure_path, 'packaged/' + fig_name)
        outfile.write(line)


def add_file_to_stream(file_name, out_stream):
    infile = open(file_name)
    for line in infile:
        depending_file = parse_line(line)
        if depending_file:
            add_file_to_stream(depending_file, out_stream)
        else:
            figure_path, fig_name = parse_for_figure(line)
            if figure_path:
                line, fig_name = remake_figure_line(line)
                shutil.copy2(figure_path, 'packaged/' + fig_name)
            out_stream.write(line)


def convert_to_one_file(file_name, out_folder):
    outfile = open(out_folder + '/' + file_name, 'w+')
    add_file_to_stream(file_name, outfile)


def make_folders(out_folder):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        # os.makedirs( outFolder + '/' + 'figures' )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    inputfilename = args.input
    outputfoldername = args.output
    # texFiles = find_file_depends( inputfilename )
    # texFiles.append( inputfilename )
    make_folders(outputfoldername)
    convert_to_one_file(inputfilename, outputfoldername)
    # for fileName in texFiles:
    #    remake_file( fileName, outputfoldername )
    # todo function for references
    shutil.copy2('references.bib', outputfoldername + '/')
