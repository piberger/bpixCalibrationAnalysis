#!/usr/bin/env python
import glob
import ROOT
import sys

# run: e.g. ./extract_roc_list.py Runs/1234 Threshold1D mean > run1234.txt
#
#  or pipe directly to ./detectorplot.py:
#    ./extract_roc_list.py Runs/758/ Threshold1D mean | ./detectorplot.py
#
# input: .root files from PixelAnalysis.exe for SCurve calibration, detectconfig.dat
# output: text file with format: ROC VALUE, e.g.
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC4 56
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC5 57
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC6 65
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC7 65

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
if statisticalProperty not in ['mean', 'rms', 'n', 'efficient', 'inefficient', 'alive', 'dead', 'extrahits']:
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

# loop over all modules in detectconfig
with open(sys.argv[1] + '/detectconfig.dat','r') as inputfile:
    for line in inputfile:
        if '_' in line:
            rocName = line.strip().split('_')
            histogramName = '/'.join(['_'.join(rocName[:i+1]) for i in range(len(rocName))])
            object = None

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
                    nTrig = calibOptions['ntrig'] if 'ntrig' in calibOptions else 10
                    for c in range(52):
                        for r in range(80):
                            if object.GetBinContent(1+c,1+r) > 0:
                                value += 1
                elif statisticalProperty == 'dead':
                    value = 0
                    nTrig = calibOptions['ntrig'] if 'ntrig' in calibOptions else 10
                    for c in range(52):
                        for r in range(80):
                            if object.GetBinContent(1+c,1+r) < 0.1:
                                value += 1
                else:
                    value = object.GetMean() if object else '-1'
            except:
                value = -999

            # skip modules with noAnalogSignal flag
            if 'noAnalog' not in '_'.join(rocName):
                if object:
                    print ('_'.join(rocName)).replace(' ','_'), value
