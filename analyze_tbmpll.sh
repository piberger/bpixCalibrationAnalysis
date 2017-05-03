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
(echo -e "SET:TITLE=$runnametext: newTBMPLLdelayX;SET:FILENAME=${runname}_tbmpll" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder SummaryTrees/SummaryInfo:newTBMPLLdelayX tree) | $DETECTORPLOTPATH/detectorplot.py
