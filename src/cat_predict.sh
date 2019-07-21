#! /bin/bash
cd ../de_novo_prediction
MAXINDEX=`find . -name "*.py" |wc -l`
File=`ls whole_predict_fasta*.txt 2>/dev/null |wc -w`
while (( $File < ${MAXINDEX} ))
do
   File=`ls whole_predict_fasta*.txt 2>/dev/null |wc -w`
   sleep 10
done
if [ $File = ${MAXINDEX} ]
 then
  for i in `ls whole_predict_fasta*.txt |sort -V`
  do
     echo "File name is: $i";
     cat $i >> whole_predict;
  done
fi


