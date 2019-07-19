#!/bin/bash
if [ $1 == local ]
  then
    bash local.sh $2 $3
elif [ $1 == LSF ]
  then
    bash submit_lsf.sh $2 $3   
else [ $1 == PBS ]
    bash submit_pbs.sh $2
fi

