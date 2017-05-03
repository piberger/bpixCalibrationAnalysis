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
(echo -e "SET:TITLE=$runnametext slope mean;SET:XBINS=256;SET:XRANGE=0,6;SET:FILENAME=${runname}_slope_mean;SET:DISTRIBUTIONS" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder Slope1D mean) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext slope rms;SET:FILENAME=${runname}_slope_rms" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder Slope1D rms) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext intercept mean;SET:FILENAME=${runname}_intercept_mean" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder Intercept1D mean) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext intercept rms;SET:FILENAME=${runname}_intercept_rms" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder Intercept1D rms) | $DETECTORPLOTPATH/detectorplot.py

