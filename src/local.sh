#!/bin/bash
start_time=`date +%s`
source activate charplant-cpu
cd ../de_novo_prediction
MAXINDEX=`find . -name "${1}*.py" |wc -l`  
[ -e /tmp/fd1 ] || mkfifo /tmp/fd1 
exec 3<>/tmp/fd1           
rm -rf /tmp/fd1     
for ((i=1;i<=${2};i++))
do
        echo >&3  
done
 
for ((i=1;i<=${MAXINDEX};i++))
do
read -u3    
{
        python ${1}${i}.py 2> /dev/null
        sleep 1
        echo 'success_'${1}${i}       
        echo >&3 
}&
done
wait
 
stop_time=`date +%s`
 
echo "TIME:`expr $stop_time - $start_time`"
exec 3<&-
exec 3>&-

