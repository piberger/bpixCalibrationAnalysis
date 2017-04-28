# bpixCalibrationAnalysis

###  tools/detectorplot.py

Creates a ROC map of full detector. ROC orientation is always 7 to 0 in the upper row and 8 to 15 in the lower one.

#### usage
````
(a) ./detectorplot.py list.txt
(b) cat list.txt | ./detectorplot.py
(c) ./detectorplot.py,  then input line by line and end with CTRL+d
````

input: .txt files created by ./extract_roc_list.py, format e.g.:
````
SET:ZRANGE=0,100
BPix_BmO_SEC1_LYR1_LDR1F_MOD2_ROC2 #
BPix_BmO_SEC1_LYR1_LDR1F_MOD2_ROC3 *
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC4 56
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC5 57
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC6 65
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC7 65
````
'#' means not tested, because masked in detectconfig, '*' means tested and flagged bad. 'SET' options are optional.

output: some colorful PDFs


### tools/extract_roc_list.py
Extract ROC list from root file Histograms *or* Tree.
#### usage
run: e.g. `./extract_roc_list.py Runs/1234 Threshold1D mean > run1234.txt`

or pipe directly to ./detectorplot.py:
````
    ./extract_roc_list.py Runs/758/ Threshold1D mean | ./detectorplot.py
````

input: .root files from PixelAnalysis.exe for SCurve calibration, detectconfig.dat
output: text file with format: ROC VALUE, e.g.
````
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC4 56
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC5 57
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC6 65
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC7 65
````

more examples:
  analyze number of pixels per ROC with >0 hits:
````
    (echo "SET:LOGZ" && ./extract_roc_list.py ../PixelAlive/Runs/Run_1094/ - alive) | ./detectorplot.py
````

all examples below are ran from run directory. `$DETECTORPLOTPATH` should point to `tools/`.

IanaBpix (extract information from tree)
````
    (echo "SET:TITLE=Run 817 new Vana" && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/SummaryInfo:newVana tree)
           | $DETECTORPLOTPATH/detectorplot.py
````
````
    (echo -e "SET:TITLE=Run 817 new Vana\nSET:XBINS=256" && $DETECTORPLOTPATH/extract_roc_list.py
           ./ SummaryTrees/SummaryInfo:newVana tree) | $DETECTORPLOTPATH/detectorplot.py
````
IanaBpix, with pass=0 ROCs flagged bad
````
(echo -e "SET:TITLE=Run 817 delta Vana\nSET:XBINS=256" && $DETECTORPLOTPATH/extract_roc_list.py ./
   SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py ./
   SummaryTrees/SummaryInfo:deltaVana tree) | $DETECTORPLOTPATH/detectorplot.py
````
TBM parameters:
````
 (echo -e "SET:TITLE=TBMADelay\n" && for i in `seq 0 15`; do grep 'TBMADelay' TBM*.dat | tr ':' ' ' |
     sed 's/TBM_module_//g' | sed 's/ TBMADelay //g' | sed "s/\.dat/_ROC$i/g"; done) |
     $DETECTORPLOTPATH/detectorplot.py
````
