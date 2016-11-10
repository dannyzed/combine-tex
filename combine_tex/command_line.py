import argparse
import re
import os
import shutil

numFiguresProcessed = 0
def parseLine( line ):
    m = re.search('input\{([^\}]*)', line)
    if m:
        return m.group(1)
    else:
        return []
def parseForFigure( line ):
    m = re.search('\{(\S*\/([^\/]*\.pdf))\}', line)
    if m:
        return m.group(1), m.group(2)
    else:
        return [], []
def remakeFigureLine( line ):
    global numFiguresProcessed
    numFiguresProcessed += 1
    figName = 'f'
    if numFiguresProcessed < 10:
        figName += '0' + str(numFiguresProcessed)
    else:
        figName += str(numFiguresProcessed)
    figName += '.pdf'
    #return re.sub(r'\{(\S*\/([^\/]*\.pdf))\}', r'{\2}', line)
    return re.sub(r'\{(\S*\/([^\/]*\.pdf))\}', '{' + figName + '}', line), figName
def findFileDepends( filename ):
    infile = open( filename )
    fileList = []
    for line in infile:
        dependingFile = parseLine( line )
        if( dependingFile != [] ):
            fileList.append( dependingFile )
            moreFiles = findFileDepends( dependingFile )
            if moreFiles != []:
                fileList.append( moreFiles )
    return fileList
def remakeFile( fileName, outFolder ):
    infile = open( fileName )
    outfile = open( outFolder + '/' + fileName, 'w+' )
    for line in infile:
        figurePath, figName = parseForFigure( line )
        if figurePath != []:
            line, figName = remakeFigureLine( line )
            shutil.copy2(figurePath, 'packaged/' + figName)
        outfile.write(line)
def addFileToStream( fileName, outStream):
    infile = open( fileName )
    for line in infile:
        dependingFile = parseLine( line )
        if( dependingFile != [] ):
            addFileToStream( dependingFile, outStream )
        else:
            figurePath, figName = parseForFigure( line )
            if figurePath != []:
                line, figName = remakeFigureLine( line )
                shutil.copy2(figurePath, 'packaged/' + figName)
            outStream.write( line )
def convertToOneFile( fileName, outFolder ):
    outfile = open( outFolder + '/' + fileName, 'w+' )
    addFileToStream( fileName, outfile )
def makeFolders( outFolder ):
    if not os.path.exists( outFolder ):
        os.makedirs( outFolder )
        #os.makedirs( outFolder + '/' + 'figures' )
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    inputfilename = args.input
    outputfoldername = args.output
    #texFiles = findFileDepends( inputfilename )
    #texFiles.append( inputfilename )
    makeFolders( outputfoldername )
    convertToOneFile( inputfilename, outputfoldername )
    #for fileName in texFiles:
    #    remakeFile( fileName, outputfoldername )
    # todo function for references
    shutil.copy2( 'references.bib', outputfoldername + '/')