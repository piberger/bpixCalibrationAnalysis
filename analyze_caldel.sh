#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
    echo "run: $0 path/Runs/Run_1234"
    exit
fi
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
runfolder=${1%/}
runname=`echo ${runfolder##*/} | tr -d '_'`
runnametext=`echo ${runfolder##*/} | tr '_' ' '`
echo $runname
(echo "SET:TITLE=$runnametext CalDel midpoint;SET:FILENAME=${runname}_caldel_midpoint" && $SCRIPTPATH/tools/extract_roc_list.py $runfolder c caldelmidpoint) | $SCRIPTPATH/tools/detectorplot.py
(echo "SET:TITLE=$runnametext CalDel width;SET:FILENAME=${runname}_caldel_width" && $SCRIPTPATH/tools/extract_roc_list.py $runfolder c caldelwidth) | $SCRIPTPATH/tools/detectorplot.py
(echo "SET:TITLE=$runnametext CalDel ineff. (middle 50%);SET:FILENAME=${runname}_caldel_inefficiency;SET:ZRANGE=0,1;SET:POSITIVE;SET:LOGZ" && $SCRIPTPATH/tools/extract_roc_list.py $runfolder c caldelinefficiency) | $SCRIPTPATH/tools/detectorplot.py
