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
extractQuantity = sys.argv[2] if len(sys.argv) > 2 else 'Threshold1D'
statisticalProperty = (sys.argv[3] if len(sys.argv) > 3 else 'mean').lower()
if statisticalProperty not in ['mean', 'rms']:
    print "unknown value:" + statisticalProperty
    exit(-2)

# search for root files
rootFileNames = glob.glob(sys.argv[1] + '/*.root')
rootFiles = [ROOT.TFile(x,'r') for x in rootFileNames]

# loop over all modules in detectconfig
with open(sys.argv[1] + '/detectconfig.dat','r') as inputfile:
    for line in inputfile:
        if '_' in line:
            rocName = line.strip().split('_')
            histogramName = '/'.join(['_'.join(rocName[:i+1]) for i in range(len(rocName))])
            object = None

            # search for module histogram in all of the root files
            for rootFile in rootFiles:
                histogramNameFull = histogramName + '_' + extractQuantity
                object = rootFile.Get(histogramNameFull)
                if object:
                    break

            # extract value from histogram
            if statisticalProperty == 'rms':
                value = object.GetRMS() if object else '-1'
            else:
                value = object.GetMean() if object else '-1'

            # skip modules with noAnalogSignal flag
            if 'noAnalog' not in '_'.join(rocName):
                if object:
                    print ('_'.join(rocName)).replace(' ','_'), value
