#!/bin/bash
cd ../de_novo_prediction
MAXINDEX=`find . -name "${1}*.py" |wc -l`
cd ../src
bash pbs.sh ${1} >run_pbs.pbs && qsub -t 1-`echo $MAXINDEX` run_pbs.pbs
