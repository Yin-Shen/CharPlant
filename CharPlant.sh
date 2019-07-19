#!/bin/bash
######
#Author: Yin Shen
#Mail: shenyin1995@163.com
######

All_step() {
snakemake -R data_preprocessing model_training motif de_novo_prediction batch_submit_job cat_predict get_positive_sample bowtie2_index bowtie2 macs2 
}

Data_preprocessing(){
snakemake -R data_preprocessing 
}

Model_training(){
snakemake -R model_training
}

Motif_visualization(){
snakemake -R motif 
}

De_novo_predicton(){
snakemake -R de_novo_prediction batch_submit_job cat_predict get_positive_sample bowtie2_index bowtie2 macs2 
}

Display_help() {
    echo "Usage: $0 [-h help]  [-s step] 
--Charplant: a de novo prediction tool of chromatin accessible regions for plant genomes" >&2
    echo '-h Show the help text'
    echo '-s The step which you want run'
    echo '''
[step] must be one of "All_step" (default), or "Data_preprocessing", "Model_training", "Motif_visualization", "De_novo_predicton"(The first two steps are required and need to be run sequentially, the next two steps are optional run)
'''
exit 1
}

step=All_step

while :
do
    case "$1" in
      -h | --help)
          Display_help
          exit 0
          ;;
      -s | --step)
           step="$2"
           shift 2
           ;;
      --) 
          shift
          break
          ;;
      -*)
          echo "Error: Unknown option: $1" >&2
          exit 1 
          ;;
      *)  
          break
          ;;
    esac
done

case "$step" in
  All_step)
    All_step
    ;;
  Data_preprocessing)
    Data_preprocessing
    ;;
  Model_training)
    Model_training
    ;;
  Motif_visualization)
    Motif_visualization
    ;;
  De_novo_predicton)
    De_novo_predicton
    ;;
 *)
     Display_help
exit 1
;;
esac
