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
(echo -e "SET:TITLE=$runnametext inefficiency;SET:ZRANGE=0.001,1;SET:LOGZ;SET:POSITIVE;SET:FILENAME=${runname}_inefficiency" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder - inefficiency) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext efficiency;SET:ZRANGE=0,1;SET:FILENAME=${runname}_efficiency" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder - efficiency) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext dead pixels;SET:ZRANGE=1,4160;SET:LOGZ;SET:POSITIVE;SET:FILENAME=${runname}_deadpixels" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder - dead) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext alive pixels;SET:ZRANGE=1,4160;SET:LOGZ;SET:POSITIVE;SET:FILENAME=${runname}_alivepixels" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder - alive) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=$runnametext extra hits;SET:FILENAME=${runname}_extrahits" && $DETECTORPLOTPATH/extract_roc_list.py $runfolder - extrahits) | $DETECTORPLOTPATH/detectorplot.py
