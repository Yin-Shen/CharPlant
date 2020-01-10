configfile: "config.yaml"

rule all:


rule data_preprocessing:
     input:
        genome=expand("{sample}", sample=config["genome"]),
        bed=expand("{sample}", sample=config["bed"]),

     params:
        out=config["out"]
     priority: 100
     shell:
        "mkdir $PWD/data_preprocessing && cd $PWD/data_preprocessing && python ../src/data_preprocess.py -g {input.genome} -b {input.bed} -o {params.out} 2> /dev/null"    
rule model_training:
     params:
        epochs=config["epochs"],
        patience=config["patience"],
        learningrate=config["learningrate"],
        batch_size=config["batch_size"],
        dropout=config["dropout"],
        nb_filter1=config["nb_filter1"],
        nb_filter2=config["nb_filter2"],
        filter_len1=config["filter_len1"],
        filter_len2=config["filter_len2"],
        hidden=config["hidden"]     
     priority: 90
     shell:
        "mkdir $PWD/model && cd $PWD/model && python ../src/model.py -e {params.epochs} -p {params.patience} -lr {params.learningrate} -b {params.batch_size} -d {params.dropout} -n1 {params.nb_filter1} -n2 {params.nb_filter2} -fl1 {params.filter_len1} -fl2 {params.filter_len2} -hd {params.hidden} 2> /dev/null"  


rule motif:       
     params:
          nb_filter1=config["nb_filter1"],
          filter_len1=config["filter_len1"],
          motif_out=config["motif_out"]
     priority: 80
     shell:
           "mkdir $PWD/motif && cd $PWD/motif && python ../src/motif.py -n1 {params.nb_filter1} -fl1 {params.filter_len1} -o {params.motif_out} 2> /dev/null"
            

rule de_novo_prediction:
     input:
         genome=expand("{sample}", sample=config["genome"]),
     params:         
         prediction_out=config["prediction_out"],
         split_lines=config["split_lines"],
         threshold=config["threshold"]
     priority: 70
     shell:
         "mkdir $PWD/de_novo_prediction && cd $PWD/de_novo_prediction && python ../src/de_novo_prediction.py -g {input.genome} -l {params.split_lines} -t {params.threshold} -o {params.prediction_out}"


rule batch_submit_job:
     params:
           run_type=config["run_type"],
           batch_submit_jobs_number=config["batch_submit_jobs_number"],
           prediction_out=config["prediction_out"]
     priority: 60
     shell:
           "cd src/ && bash batch_submit.sh {params.run_type} {params.prediction_out} {params.batch_submit_jobs_number}"

rule cat_predict:
     priority: 50
     shell:
          "cd src/ && bash cat_predict.sh"

rule get_positive_sample:
       params:
         prediction_out=config["prediction_out"],
         speices_name=config["speices_name"]
       priority: 40
       shell: 
           "python src/get_positive_sample.py -i {params.prediction_out} -n {params.speices_name}"

rule bowtie2_index:
      input:
        genome=expand("{sample}", sample=config["genome"])
      params:
        index_name=config["index_name"]
      priority: 30
      threads: 16
      shell:
          " mkdir $PWD/peak && cd $PWD/peak && bowtie2-build {input.genome}  {params.index_name}"


rule bowtie2:
     params:
        index_name=config["index_name"],
        sam_prefix=config["sam_prefix"]
     priority: 20
     threads: 16
     shell:
          "cd $PWD/peak && bowtie2 -x {params.index_name}  -f ../de_novo_prediction/whole_pre.fa -S {params.sam_prefix}.sam "


rule macs2:
    params:
        sam_prefix=config["sam_prefix"],
        peak_prefix=config["peak_prefix"]      
    priority: 10
    threads: 16
    shell:
          "cd $PWD/peak && source activate macs2 && macs2 callpeak -t {params.sam_prefix}.sam  -f SAM --shift -125 --extsize 250 --nomodel -B --SPMR -g hs -n {params.peak_prefix} "
         
