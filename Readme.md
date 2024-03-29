<img width="200px" src="https://raw.githubusercontent.com/Yin-Shen/CharPlant/master/logo.jpg" />


# Introduction <br>
The result of OCR (Open Chromatin Region) assay technologies such as DNase-seq and ATAC-seq represents the open state of a tissue at a given time and does not cover all the chromatin accessible information of this species. To predict the potential open regions of different tissues at different times in the whole sequence can help to understand gene transcription and regulation from a global perspective. **CharPlant** (Chromatin Accessible Regions for Plant) is a *de novo* OCRs prediction tool based on deep learning model. It can take complete DNA sequences or scaffolds as input, and output the outline of OCRs in a .Bed format file rely on sequence features. To our knowledge, this is the first tool to *de novo* predict potential open chromatin regions from DNA sequence and assay data.<br>
## If you use this tool, please cite the following article:
[CharPlant: A De Novo Open Chromatin Region Prediction Tool for Plant Genomes](https://www.sciencedirect.com/science/article/pii/S1672022921000401)

# Steps to install and run CharPlant <br>
CharPlant currently available for Linux-based platforms. It can learn the OCR features from DNase-seq or ATAC-seq data and *de novo* predict potential chromatin open regions for plant genome. To train the parameters of the deep learning model and predict OCRs, CharPlant perform the following three steps. Step 1 and step 2 are to  install needed packages and set up running environment of the software, and they are optional for the users have had those packages worked. Step 3 is to download and run CharPlant. We provide as detailed instruction as possible although it can be run using simple command line. In the following, prompt “$” starts a shell command line of  Linux, while “#” starts a comment.

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
* numpy(1.16.1)
* matplotlib(3.3.2)
* pyfiglet(0.8.post1)
* sklearn(0.22)
* keras(2.0.5)
* h5py(2.7.1)
* tensorflow-gpu(1.3.0)

### (iii) create environments
Because the *de novo* prediction  step using cpu, we need create environments in cpu
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
$ pip install snakemake==5.5.2
```

## Step 3. Download and run CharPlant

### (i) Download and install CharPlant
To Install and run CharPlant is very easy. You can download the CharPlant package in  the following two ways. Then un-compress the package and set “CharPlant” as current directory. 

* Simple click to download CharPlant package [HERE](http://cbi.hzau.edu.cn/CharPlant/data/CharPlant.tar.gz). 
* You can also download the CharPlant package using git.

```
$ git clone https://github.com/Yin-Shen/CharPlant.git
```
```
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
Configuration file “config.yaml” contains all parameters of the tool. To run CharPlant, you only need to revise three parameters in the following according to your path and file name, while leaving others as they are. A complete “config.yaml” file is shown in next section.
```
genome :  Yourpath/CharPlant/example/oryza_sativa.fa             #Genome file in .fasta format for input(Need full path)
bed:  Yourpath/CharPlant/example/oryza_sativa.bed                #Open chromatin regions file in .bed format for input(Need full path)
out: ory                                                         #Prefix of the output file
```
### (iv) Run CharPlant 
Snakemake file defines rules to performance operations. We have created a rule for each target and intermediate file. It is not necessary for the users to rewrite it. A complete “Snakefile” file is shown in subsequent section.
```
$ CharPlant.sh
```
CharPlant will perform four steps in turn and output the results of predicted OCRs to a .bed format file.
* **Data preprocessing**
* **Model training**
* **Motif visualization**
* ***De novo* prediction**

### (v) Output files
If all steps are completed, the results will be output to the following five directories.
```
/data_preprocessing---Data preprocessing results for model training and motif visualization.
/model---.json file of model architecture, .h5 file of model parameters and .png file of the result figure.
/motif--- Positional weight matrix of motifs.
/de_novo_prediction---Results of de novo prediction.
/peak---Peaks of predicted OCRs.
```

# Contact us

**Yin Shen**: shenyin1995@163.com <br>
**Ling-Ling Chen**: llchen@mail.hzau.edu.cn <br>
**Junxiang Gao**: gao200@mail.hzau.edu.cn <br>

