#!/usr/bin/env python
import glob
import ROOT
import sys

# usage: see README.md

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
if statisticalProperty not in ['mean', 'rms', 'n', 'efficient', 'inefficient', 'alive', 'dead', 'extrahits', 'deltaiana','tree','meanoccupancy'] and not statisticalProperty.startswith('occupancy'):
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
                rocNameTree = object.rocName.split('\x00')[0].strip()
                if rocNameTree not in treeData:
                   treeData[rocNameTree] = object.__getattr__(branchname)

# loop over all modules in detectconfig
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
                    object = None

            else:
                # search for module histogram in all of the root files
                for rootFile in rootFiles:
                    histogramNameFull = histogramName + '_' + extractQuantity if len(extractQuantity) > 0 else histogramName
                    object = rootFile.Get(histogramNameFull)
                    if object:
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
                    elif statisticalProperty.startswith('meanoccupancy'):
                        value = 0
                        for c in range(52):
                            for r in range(80):
                                # bin content is between 0 and 100.
                                value += object.GetBinContent(1+c, 1+r)
                        value /= 416000.0
                    elif statisticalProperty == 'dead':
                        value = 0
                        for c in range(52):
                            for r in range(80):
                                if object.GetBinContent(1+c,1+r) < 0.1:
                                    value += 1
                    elif statisticalProperty == 'deltaiana':
                        f2 = object.Get('f2')
                        print f2
                    else:
                        value = object.GetMean() if object else '-1'
                except:
                    value = -999

            # skip modules with noAnalogSignal flag
            if object or value == '#':
                print ('_'.join(rocName)).replace(' ','_'), value
