echo "#!/bin/sh"
echo "#PBS -N predict"
echo "#PBS -l nodes=1:ppn=1"
echo "#PBS -l walltime=1200:00:00"
echo "#PBS -q batch"
echo "#PBS -V"
echo "#PBS -S /bin/bash"
echo "source activate charplant-cpu"
echo "cd $PBS_O_WORKDIR"
echo "cd ../de_novo_prediction"
echo "python ${1}\${PBS_ARRAYID}.py"