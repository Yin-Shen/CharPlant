#!/bin/bash
cd ../de_novo_prediction
MAXINDEX=`find . -name "${1}*.py" |wc -l`
cd ../src
bash lsf.sh $1 $2 >run_lsf.sh && bsub -J "run_lsf[1-`echo $((MAXINDEX/${2} +1))`]" < run_lsf.sh
