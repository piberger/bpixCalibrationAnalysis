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
(echo -e "SET:TITLE=dac/$runnametext Vana;SET:FILENAME=dac_${runname}_vana" && grep 'ROC:\|Vana' ${runfolder}/ROC*.dat | awk '{print $2}' | sed 'N;s/\n/ /') | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=dac/$runnametext CalDel;SET:FILENAME=dac_${runname}_caldel" && grep 'ROC:\|CalDel' ${runfolder}/ROC*.dat | awk '{print $2}' | sed 'N;s/\n/ /') | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=dac/$runnametext Vdd;SET:FILENAME=dac_${runname}_vdd" && grep 'ROC:\|Vdd' ${runfolder}/ROC*.dat | awk '{print $2}' | sed 'N;s/\n/ /') | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=dac/$runnametext PHScale;SET:FILENAME=dac_${runname}_phscale" && grep 'ROC:\|PHScale' ${runfolder}/ROC*.dat | awk '{print $2}' | sed 'N;s/\n/ /') | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=dac/$runnametext PHOffset;SET:FILENAME=dac_${runname}_phoffset" && grep 'ROC:\|PHOffset' ${runfolder}/ROC*.dat | awk '{print $2}' | sed 'N;s/\n/ /') | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=dac/$runnametext VcThr;SET:FILENAME=dac_${runname}_vcthr" && grep 'ROC:\|VcThr' ${runfolder}/ROC*.dat | awk '{print $2}' | sed 'N;s/\n/ /') | $DETECTORPLOTPATH/detectorplot.py

