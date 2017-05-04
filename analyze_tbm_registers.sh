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
(echo -e "SET:TITLE=tbm/$runnametext TBMPLLDelay;SET:FILENAME=tbm_${runname}_tbmplldelay" && grep 'TBMPLLDelay' ${runfolder}/TBM*.dat | tr ':' ' ' | sed 's/TBM_module_//g' | sed 's/ TBMPLLDelay //g' | sed "s/\.dat//g" | awk '{n=split($1, array, "/"); print array[n]" "$2}' | $DETECTORPLOTPATH/module2roclist.py) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=tbm/$runnametext TBMADelay;SET:FILENAME=tbm_${runname}_tbmadelay" && grep 'TBMADelay' ${runfolder}/TBM*.dat | tr ':' ' ' | sed 's/TBM_module_//g' | sed 's/ TBMADelay //g' | sed "s/\.dat//g" | awk '{n=split($1, array, "/"); print array[n]" "$2}' | $DETECTORPLOTPATH/module2roclist.py) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=tbm/$runnametext TBMA token Delay;SET:FILENAME=tbm_${runname}_tbmatokendelay" && grep 'TBMADelay' ${runfolder}/TBM*.dat | tr ':' ' ' | sed 's/TBM_module_//g' | sed 's/ TBMADelay //g' | sed "s/\.dat//g" | awk '{n=split($1, array, "/");b=int($2/128); print array[n]" "b}' | $DETECTORPLOTPATH/module2roclist.py) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=tbm/$runnametext TBMA header/trailer Delay;SET:FILENAME=tbm_${runname}_tbmahtdelay" && grep 'TBMADelay' ${runfolder}/TBM*.dat | tr ':' ' ' | sed 's/TBM_module_//g' | sed 's/ TBMADelay //g' | sed "s/\.dat//g" | awk '{n=split($1, array, "/");b=int(($2-(int($2/128)*128))/64); print array[n]" "b}' | $DETECTORPLOTPATH/module2roclist.py) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=tbm/$runnametext TBMA port1 Delay;SET:FILENAME=tbm_${runname}_tbmap1delay;SET:PALETTE=rainbow2;SET:ZRANGE=-0.001,7" && grep 'TBMADelay' ${runfolder}/TBM*.dat | tr ':' ' ' | sed 's/TBM_module_//g' | sed 's/ TBMADelay //g' | sed "s/\.dat//g" | awk '{n=split($1, array, "/");b=int($2);if(b>=128)b=b-128;if(b>=64)b=b-64;b=int(b/8); print array[n]" "b}' | $DETECTORPLOTPATH/module2roclist.py) | $DETECTORPLOTPATH/detectorplot.py
(echo -e "SET:TITLE=tbm/$runnametext TBMA port0 Delay;SET:FILENAME=tbm_${runname}_tbmap0delay;SET:PALETTE=rainbow2;SET:ZRANGE=-0.001,7" && grep 'TBMADelay' ${runfolder}/TBM*.dat | tr ':' ' ' | sed 's/TBM_module_//g' | sed 's/ TBMADelay //g' | sed "s/\.dat//g" | awk '{n=split($1, array, "/");b=int($2);if(b>=128)b=b-128;if(b>=64)b=b-64;if(b>=32)b=b-32;if(b>=16)b=b-16;if(b>=8)b=b-8; print array[n]" "b}' | $DETECTORPLOTPATH/module2roclist.py) | $DETECTORPLOTPATH/detectorplot.py

