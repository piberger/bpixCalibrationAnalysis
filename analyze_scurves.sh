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
(echo -e "SET:TITLE=$runnametext threshold;SET:FILENAME=${runname}_threshold" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder Threshold1D mean) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext noise;SET:FILENAME=${runname}_noise" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder Noise1D mean) | $DETECTORPLOTPATH/detectorplot.py
