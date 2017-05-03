# bpixCalibrationAnalysis

###  tools/detectorplot.py

Creates a ROC map of full detector. ROC orientation is always 7 to 0 in the upper row and 8 to 15 in the lower one.

#### usage
````
(a) tools/detectorplot.py list.txt
(b) cat list.txt | tools/detectorplot.py
(c) tools/detectorplot.py,  then input line by line and end with CTRL+d
````

input: .txt files created by ./extract_roc_list.py, format e.g.:
````
SET:ZRANGE=0,100
SET:LOGZ
SET:TITLE=Plot title here
BPix_BmO_SEC1_LYR1_LDR1F_MOD2_ROC2 #
BPix_BmO_SEC1_LYR1_LDR1F_MOD2_ROC3 *
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC4 56
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC5 57
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC6 65
BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC7 65
````
'#' means not tested, because masked in detectconfig, '*' means tested and flagged bad. 'SET' options are optional.

options:
````
ZRANGE=..       z axis range
XRANGE=..       x axis range for 1D distributions
LOGZ            log scale
TITLE=..        plot title
PALETTE=..      root palette number, 55 for "rain bow", 'rainbow' for blue->red rainbow
LYR1            only plot LYR1
LYR2            only plot LYR2
LYR3            only plot LYR3
LYR4            only plot LYR4
DISTRIBUTIONS   plot 1D distributions
````
output: some colorful PDFs

#### example

````
tools/detectorplot.py examples/test.txt
````

more examples below!

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

**IanaBpix** (extract information from tree)
````
    (echo "SET:TITLE=Run 817 new Vana" && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/SummaryInfo:newVana tree)
           | $DETECTORPLOTPATH/detectorplot.py
````
````
    (echo -e "SET:TITLE=Run 817 new Vana\nSET:XBINS=256" && $DETECTORPLOTPATH/extract_roc_list.py
           ./ SummaryTrees/SummaryInfo:newVana tree) | $DETECTORPLOTPATH/detectorplot.py
````
**IanaBpix**, with pass=0 ROCs flagged bad
````
(echo -e "SET:TITLE=Run 817 delta Vana\nSET:XBINS=256" && $DETECTORPLOTPATH/extract_roc_list.py ./
   SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py ./
   SummaryTrees/SummaryInfo:deltaVana tree) | $DETECTORPLOTPATH/detectorplot.py
````
**IanaBpix**, make separate plots for each layer:
````
(echo -e "SET:TITLE=Run 817 delta Vana LYR1;SET:LYR1;SET:FILENAME=run817_lyr1_deltavana" && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/SummaryInfo:deltaVana tree) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=Run 817 delta Vana LYR2;SET:LYR2;SET:FILENAME=run817_lyr2_deltavana" && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/SummaryInfo:deltaVana tree) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=Run 817 delta Vana LYR3;SET:LYR3;SET:FILENAME=run817_lyr3_deltavana" && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/SummaryInfo:deltaVana tree) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=Run 817 delta Vana LYR4;SET:LYR4;SET:FILENAME=run817_lyr4_deltavana" && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/SummaryInfo:deltaVana tree) | $DETECTORPLOTPATH/detectorplot.py
````
**TBM** parameters (from config/tbm/n/ folder):
````
 (echo -e "SET:TITLE=TBMADelay\n" && for i in `seq 0 15`; do grep 'TBMADelay' TBM*.dat | tr ':' ' ' |
     sed 's/TBM_module_//g' | sed 's/ TBMADelay //g' | sed "s/\.dat/_ROC$i/g"; done) |
     $DETECTORPLOTPATH/detectorplot.py
````
**TBMPLLNoTokenPass** scan:
````
    (echo -e "SET:TITLE=Run 1108: newTBMPLLdelayX\n" && $DETECTORPLOTPATH/extract_roc_list.py ./ SummaryTrees/SummaryInfo:newTBMPLLdelayX tree) |
    $DETECTORPLOTPATH/detectorplot.py
````
**PixelAlive** inefficiency, log scale:
````
    (echo -e "SET:TITLE=Run 1018 inefficiency\nSET:ZRANGE=0.001,1\nSET:LOGZ\nSET:POSITIVE\n" && $DETECTORPLOTPATH/extract_roc_list.py ./ - inefficiency) |
    $DETECTORPLOTPATH/detectorplot.py
````
**SCurve** threshold:
````
    (echo -e "SET:TITLE=Run 1093 threshold\n" && $DETECTORPLOTPATH/extract_roc_list.py ./ Threshold1D mean) | $DETECTORPLOTPATH/detectorplot.py
````
**SCurve** noise:
````
    (echo -e "SET:TITLE=Run 1093 noise\n" && $DETECTORPLOTPATH/extract_roc_list.py ./ Noise1D mean) | $DETECTORPLOTPATH/detectorplot.py
````