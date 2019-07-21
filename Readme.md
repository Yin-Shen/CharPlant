# CharPlant
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3344985.svg)](https://doi.org/10.5281/zenodo.3344985) <br>

# Introduction <br>
The result of OCR (Open Chromatin Region) assay technologies such as DNase-seq and ATAC-seq represents the open state of a tissue at a given time and does not cover all the chromatin accessible information of this species. To predict the potential open regions of different tissues at different times in the whole sequence can help to understand gene transcription and regulation from a global perspective. **CharPlant** (Chromatin Accessible Regions for Plant) is a de novo OCRs prediction tool based on deep learning model. It can take complete DNA sequences or scaffolds as input, and output the outline of OCRs in a .Bed format file rely on sequence features. To our knowledge, this is the first software to de novo predict potential open chromatin regions from DNA sequence and assay data.<br>
&emsp;&emsp;When using the tool, kindly acknowledge the project contribution by citing the following papers: Yin Shen, Ling-Ling Chen, and Junxiang Gao*. CharPlant: a de novo prediction tool of chromatin accessible regions for plant genomes. (Submitted to *Plant Biotechnology Journal*)


# Steps to install and run CharPlant <br>
CharPlant currently available for Linux-based platforms. It can learn the OCR features from DNase-seq or ATAC-seq data and de novo predict potential chromatin open regions for plant genome. To train the parameters of the deep learning model and predict OCRs, CharPlant perform the following three steps. Step 1 and step 2 are to  install needed packages and set up running environment of the software, and they are optional for the users have had those packages worked. Step 3 is to download and run CharPlant. We provide as detailed instruction as possible although it can be run using simple command line. In the following, prompt “$” starts a shell command line of  Linux, while “#” starts a comment.



## Step 1. Install python packages
CharPlant is developed in python language, and some fundamental packages for  scientific computing and network construction are indispensable. To efficient install and manage them, we strongly recommend using the **Conda** package manager. Conda is an open source package and environment management system for installing multiple versions of packages and their dependencies and easily switching between them.

### (i) Install Conda
```
$ wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
$ bash Anaconda3-4.2.0-Linux-x86_64.sh
#Add environment variable
$ echo "export PATH=\"${PWD}/anaconda3/bin:\$PATH\" " >>~/.bashrc
$ source ~/.bashrc
```

### (ii) Install needed python packages
Following Python packages are required:
* numpy
* matplotlib
* pyfiglet
* sklearn
* keras
* tensorflow-gpu

### (iii) create environments
Because the de novo prediction  step using cpu, we need create environments in cpu
```
$ conda create --name charplant-cpu python=3.6
$ source activate charplant-cpu
$ pip install sklearn
$ pip install matplotlib
$ pip install pyfiglet
$ conda install keras
$ source deactivate charplant-cpu
```
## Step 2. Install the tools Bowtie2 , MACS2 and Snakemake
### (i)Bowtie2
We use bowtie2 (version 2.2.6) for sequence alignment, and you can find all versions [HERE](https://sourceforge.net/projects/bowtie-bio/files/bowtie2/). The detailed manual is provided in this [LINK](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml).

```
$ wget https://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.6/bowtie2-2.2.6-linux-x86_64.zip
$ unzip bowtie2-2.2.6-linux-x86_64.zip
#Add environment variable
$ echo "export PATH=\"${PWD}/bowtie2-2.2.6:\$PATH\" " >>~/.bashrc
$ source ~/.bashrc
```
### (ii)MACS2
We use MACS2 (version 2.1.1) for peak calling, and you can find all versions and  user manual [HERE](https://pypi.org/project/MACS2/2.0.10.20130915/#history). 
```
$ wget https://files.pythonhosted.org/packages/0f/e9/60761f3df0634a50a96531fdb00f45dd3a6f3aa2509fb722eb2a665faf35/MACS2-2.1.1.20160226.tar.gz
$ tar -zxvf  MACS2-2.1.1.20160226.tar.gz
#setup environment variable
$ conda create --name macs2 python=2.7
$ source activate macs2
$ cd MACS2-2.1.1.20160226
$ pip install numpy
$ python setup.py install 
#deactivate the environment 
$ source deactivate macs2
```
### (iii)Snakemake
We adopt an easy-to-use workflow software Snakemake to build our analysis  process, which combines a series of steps into a single pipeline. Snakemake and the  manual are provided in this [LINK](https://snakemake.readthedocs.io/en/stable/index.html). 
```
$ pip install snakemake
```

## Step 3. Download and run CharPlant

### (i) Download and install CharPlant
To Install and run CharPlant is very easy. You can download the CharPlant package in  the following two ways. Then un-compress the package and set “charplant” as current directory. 

* Simple click to download CharPlant package [HERE](http://cbi.hzau.edu.cn/CharPlant/data/CharPlant.tar.gz). 
* You can also download the CharPlant package using wget or through git.
```
$ wget http://cbi.hzau.edu.cn/CharPlant/data/CharPlant.tar.gz
```
or
```
$ git clone https://github.com/Yin-Shen/CharPlant
```
```
$ tar -zxvf  CharPlant.tar.gz
$ echo "export PATH=\"${PWD}/CharPlant:\$PATH\" " >>~/.bashrc
$ source ~/.bashrc
$ cd CharPlant
$ chmod -R 744 CharPlant.sh
```
### (ii) The directory structure of CharPlant
The directory structure is as follows, which has two directories and three files. Directory “CharPlant/example” contains the reference genome and DNase-seq data of rice used as an example, file oryza_sativa.fa and ory_sativa.bed, respectively. The result of predicted OCRs is also saved in it. All the python and shell scripts are in directory “CharPlant/src”, but users generally don't need to care about it. 
```
├──CharPlant
│       ├── example
│       │       ├──oryza_sativa.bed
│       │       ├──oryza_sativa.fa
│       ├── src 
│       │       ├──data_preprocess
│       │       ├──de_novo_prediction
│       │       ├──get_positive_sample
│       │       ├──model
│       │       ├──motif
…       …       …      …
│       │       ├──submit_lsf
│   ├── config.yaml
│   ├── Snakefile 
│   ├── CharPlant.sh
```
For example, the follow command can print help information.
```
$ CharPlant.sh -h
```
Or print python scripts help information.
```
$ python model.py -h
```
### (iii) Set the parameters of CharPlant
To run Charplant, you need to make a minor revision to the configuration file “config.yaml”. This file is the only one should be modified because it contains all parameters of CharPlant. For the vast majority of the parameters, you just leave them as they are to use the default value we provided. Only three parameters in the following need to be modified. 
```
genome :  Yourpath/CharPlant/example/oryza_sativa.fa             #Genome file in .fasta format for input(Need full path)
bed:  Yourpath/CharPlant/example/oryza_sativa.bed                #Open chromatin regions file in .bed format for input(Need full path)
out: ory                                                         #Prefix of the output file
```
### (iv) Run CharPlant 
Snakefile defines rules to performance operations. For each target and intermediate file, we have created rules that defined how they are created from input files. It is not necessary for the users of CharPlant to rewrite it except for executing a single line of command.
```
$ CharPlant.sh
```
CharPlant will perform four steps in turn and output the results of predicted OCRs to a .bed format file.
* **Data preprocessing**
* **Model training**
* **Motif visualization**
* **De novo predicton**

### (v) Output files
If all is successful, you will get the result in the following directory structure.

* **[data_preprocessing]** Data preprocessing Results file for model training and motif visualization.
* **[model]**  .json file of model architecture , .h5 file of model parameters and .png file of the result figure.
* **[motif]** Motif's positional weight matrix file.
* **[de_novo_prediction]** Results file for de novo prediction in the whole genome.
* **[peak]** The result of predicted OCRs is  saved in it.


# Contact us

**Yin Shen**: 1490025927@qq.com <br>
**Ling-Ling Chen**: llchen@mail.hzau.edu.cn <br>
**Junxiang Gao**: gao200@mail.hzau.edu.cn <br>

