#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
    echo "run: $0 path/Runs/Run_1234"
    exit
fi
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
runfolder=${1%/}
runname=`echo ${runfolder##*/} | tr -d '_'`
runnametext=`echo ${runfolder##*/} | tr '_' ' '`
DETECTORPLOTPATH=$SCRIPTPATH/tools
echo $runname
(echo -e "SET:TITLE=$runnametext delta Vana;SET:XBINS=256;SET:FILENAME=${runname}_deltavana" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/SummaryInfo:deltaVana tree) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext new Vana;SET:XBINS=256;SET:DISTRIBUTIONS;SET:FILENAME=${runname}_newvana" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/SummaryInfo:newVana tree) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext new Iana;SET:ZRANGE=22,26;SET:FILENAME=${runname}_newiana" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/SummaryInfo:newIana tree) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext RB efficiency;SET:FILENAME=${runname}_rbefficiency" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/PassState:pass tree | grep 0.0 | awk '{print $1 " *"}' && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/PassState:efficiency tree) | $DETECTORPLOTPATH/detectorplot.py