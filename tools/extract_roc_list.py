#!/usr/bin/env python
import glob
import ROOT
import sys
import os

# usage: see README.md

def get_caldel_range(object):
    binsX = object.GetXaxis().GetNbins()
    startPosition = 0
    endPosition = 0
    startFound = False
    endFound = False
    maxEfficiency = object.GetBinContent(object.GetMaximumBin())

    # limit efficiency to 100%, additional unwanted hits can now be detected with 'caldelextrahits' option!
    if maxEfficiency > 1.0:
        maxEfficiency = 1.0

    for c in range(binsX):
        count = object.GetBinContent(1 + c, 1)
        if not startFound and count > 0.9 * maxEfficiency:
            startFound = True
            startPosition = c
        if startFound and not endFound and c - startPosition > 5 and count > 0.9 * maxEfficiency:
            endPosition = c
        if startFound and not endFound and c - startPosition > 5 and count < 0.1 * maxEfficiency:
            endFound = True
            if endPosition < 1:
                endPosition = c
        if startFound and endFound:
            break
    return [startPosition, endPosition]

def get_caldel_efficiency(object, startPosition, endPosition):
    efficiencies = []
    for c in range(startPosition, endPosition+1):
        efficiencies.append(object.GetBinContent(1 + c, 1))
    return 1.0*sum(efficiencies)/len(efficiencies) if len(efficiencies) > 0 else -1

def get_caldel_bins_above_one(object, startPosition, endPosition):
    nBinsAboveOne = 0
    for c in range(startPosition, endPosition+1):
        if object.GetBinContent(1 + c, 1) > 1.0:
            nBinsAboveOne += 1
    return nBinsAboveOne


if len(sys.argv) < 2:
    print "usage: %s path/to/runfolder/with/root/files [Quantity] [mean/rms]"%sys.argv[0]
    print "e.g. %s runs/1234 Threshold1D mean"%sys.argv[0]
    print "needed files in run folder: SCurve_*_Run_*.root, detectconfig.dat"
    exit(-1)

# verify command line arguments
extractQuantity = (sys.argv[2] if len(sys.argv) > 2 else 'Threshold1D').strip()
if extractQuantity == '-':
    extractQuantity = ''
statisticalProperty = (sys.argv[3] if len(sys.argv) > 3 else 'mean').lower()
if statisticalProperty not in ['mean', 'rms', 'n', 'efficient', 'inefficient', 'alive', 'dead', 'extrahits', 'deltaiana','tree','meanoccupancy','efficiency','inefficiency','caldelmidpoint','caldelwidth','caldelefficiency','caldelinefficiency','caldelextrahits'] and not statisticalProperty.startswith('occupancy'):
    print "unknown value:" + statisticalProperty
    exit(-2)

# search for root files
rootFileNames = glob.glob(sys.argv[1] + '/*.root')
rootFiles = [ROOT.TFile(x,'r') for x in rootFileNames]

# calib.dat
calibOptions = {}
try:
    with open(sys.argv[1] + '/calib.dat','r') as inputfile:
        readValue = None
        for line in inputfile:
            if readValue == 'ntrig':
                calibOptions['ntrig'] = int(line)
                readValue = None

            if line.strip().lower().split(':')[0] == 'repeat':
                readValue = 'ntrig'
except:
    pass

treeData = {}
if statisticalProperty == 'tree':

    for rootFile in rootFiles:
        treeName = extractQuantity.split(':')[0]
        branchname = extractQuantity.split(':')[1]
        object = rootFile.Get(treeName)
        if object:
            for evt in object:
                # strings are terminated by \x00 characters, with garbage after
                try:
                    rocNameTree = object.rocName.split('\x00')[0].strip()

                    if rocNameTree not in treeData:
                       treeData[rocNameTree] = object.__getattr__(branchname)
                except:
                    moduleNameTree = object.moduleName.split('\x00')[0].strip()

                    if 'LYR1' in moduleNameTree and 'H_' in moduleNameTree:
                        rocsList = [4, 5, 6, 7, 8, 9, 10, 11]
                    elif 'LYR1' in moduleNameTree and 'F_' in moduleNameTree:
                        rocsList = [0, 1, 2, 3, 12, 13, 14, 15]
                    else:
                        rocsList = [0, 1, 2, 3, 12, 13, 14, 15, 4, 5, 6, 7, 8, 9, 10, 11]

                    for i in rocsList:
                        rocNameTree = moduleNameTree + "_ROC%d"%i
                        if rocNameTree not in treeData:
                           treeData[rocNameTree] = object.__getattr__(branchname)


# loop over all modules in detectconfig
if not os.path.isfile(sys.argv[1] + '/detectconfig.dat'):
    print >> sys.stderr, "\x1b[31mERROR: detectconfig.dat missing in run directory!\x1b[0m"
    print "ERROR"
    exit(0)

with open(sys.argv[1] + '/detectconfig.dat','r') as inputfile:
    for line in inputfile:
        if '_' in line:
            rocName = line.strip().split('_')
            rocNameJoined = '_'.join(rocName)
            histogramName = '/'.join(['_'.join(rocName[:i+1]) for i in range(len(rocName))])
            object = None

            if 'noAnalogSignal' in line:
                value = '#'
            elif statisticalProperty == 'tree':
                #
                if rocNameJoined in treeData:
                    value = treeData[rocNameJoined]
                    object = True
                else:
                    print >> sys.stderr, "\x1b[31mWARNING: roc was not found in root trees:", rocNameJoined, "\x1b[0m"
                    value = -1
                    object = None

            else:
                # search for module histogram in all of the root files
                for rootFile in rootFiles:
                    histogramNameFull = histogramName + '_' + extractQuantity if len(extractQuantity) > 0 else histogramName
                    object = rootFile.Get(histogramNameFull)
                    if object:
                        if type(object) is ROOT.TCanvas:
                            canvasObject = object
                            for i in canvasObject.GetListOfPrimitives():
                                if i.GetName().strip() == histogramName.split('/')[-1].strip():
                                    object = i
                                    break
                            if object:
                                break

                        else:
                            break

                # extract value from histogram
                try:
                    if statisticalProperty == 'rms':
                        value = object.GetRMS() if object else '-1'
                    elif statisticalProperty == 'n':
                        value = object.GetEntries() if object else '-1'
                    elif statisticalProperty == 'efficient':
                        value = 0
                        nTrig = calibOptions['ntrig'] if 'ntrig' in calibOptions else 10
                        for c in range(52):
                            for r in range(80):
                                if object.GetBinContent(1+c,1+r) == 100.0:
                                    value += 1
                    elif statisticalProperty == 'extrahits':
                        value = 0
                        nTrig = calibOptions['ntrig'] if 'ntrig' in calibOptions else 10
                        for c in range(52):
                            for r in range(80):
                                if object.GetBinContent(1+c,1+r) > 100.0:
                                    value += 1
                    elif statisticalProperty == 'inefficient':
                        value = 0
                        nTrig = calibOptions['ntrig'] if 'ntrig' in calibOptions else 10
                        for c in range(52):
                            for r in range(80):
                                if object.GetBinContent(1+c,1+r) < 100.0:
                                    value += 1
                    elif statisticalProperty == 'alive':
                        value = 0
                        for c in range(52):
                            for r in range(80):
                                if object.GetBinContent(1+c,1+r) > 0:
                                    value += 1
                    elif statisticalProperty.startswith('occupancy'):
                        minOccupancy = float(statisticalProperty[9:])
                        value = 0
                        for c in range(52):
                            for r in range(80):
                                # minOccupancy is given as fraction between 0 and 1, bin content is between 0 and 100.
                                if object.GetBinContent(1+c,1+r) >= minOccupancy*100:
                                    value += 1
                    elif statisticalProperty.startswith('meanoccupancy') or statisticalProperty.startswith('efficiency'):
                        value = 0
                        for c in range(52):
                            for r in range(80):
                                # bin content is between 0 and 100.
                                value += object.GetBinContent(1+c, 1+r)
                        value /= 416000.0
                    elif statisticalProperty.startswith('inefficiency'):
                        value = 0
                        for c in range(52):
                            for r in range(80):
                                # bin content is between 0 and 100.
                                value += object.GetBinContent(1+c, 1+r)
                        value /= 416000.0
                        value = 1.0 - value
                    elif statisticalProperty == 'dead':
                        value = 0
                        for c in range(52):
                            for r in range(80):
                                if object.GetBinContent(1+c,1+r) < 0.1:
                                    value += 1
                    elif statisticalProperty == 'deltaiana':
                        f2 = object.Get('f2')
                        print f2
                    elif statisticalProperty == 'caldelmidpoint':
                        caldelRange = get_caldel_range(object)
                        value = (caldelRange[1]+caldelRange[0])/2.0
                    elif statisticalProperty == 'caldelwidth':
                        caldelRange = get_caldel_range(object)
                        value = (caldelRange[1]-caldelRange[0])
                    elif statisticalProperty == 'caldelefficiency':
                        caldelRange = get_caldel_range(object)
                        value = get_caldel_efficiency(object, caldelRange[0], caldelRange[1])
                    elif statisticalProperty == 'caldelinefficiency':
                        caldelRange = get_caldel_range(object)
                        width = (caldelRange[1]-caldelRange[0])
                        startPos = int(caldelRange[0] + width * 0.25)
                        endPos = int(caldelRange[0] + width * 0.75)
                        value = 1.0-get_caldel_efficiency(object, startPos, endPos)
                    elif statisticalProperty == 'caldelextrahits':
                        caldelRange = get_caldel_range(object)
                        width = (caldelRange[1]-caldelRange[0])
                        startPos = int(caldelRange[0] + width * 0.05)
                        endPos = int(caldelRange[0] + width * 0.95)
                        value = get_caldel_bins_above_one(object, startPos, endPos)
                    else:
                        value = object.GetMean() if object else '-1'
                except Exception as e:
                    print "EXCEPTION:", e
                    value = -999

            # skip modules with noAnalogSignal flag
            if object or value == '#':
                print ('_'.join(rocName)).replace(' ','_'), value
