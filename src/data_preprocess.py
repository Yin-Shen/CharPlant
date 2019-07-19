'''
This script is preprocess data for charplant cnn model

Author: Yin Shen
'''

#Required Modules
import numpy as np
import re
import random
import pyfiglet
import argparse
import os
import sklearn
from sklearn.model_selection import train_test_split

#Making large letters out of ordinary text with pyfiglet
ascii_banner = pyfiglet.figlet_format("charplant")
print(ascii_banner)

#Argument parsing
parser = argparse.ArgumentParser(description='''Data Preprocess: 
                                                takes 3 required arguments''')
parser.add_argument("--genome", "-g", required=True,
                    help="genome file in fasta format")
parser.add_argument("--bed", "-b", required=True,
                    help="bed file of Chromatin Accessible Regions for input")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()

#Construct a positive sample sequences
genome_fasta={}
for line in open(args.genome,'r'):
    if line[0]=='>':
        seq_name=line.lstrip('>').strip()
        genome_fasta[seq_name]=[]
    else:
        genome_fasta[seq_name].append(line.strip())
for keys,val in genome_fasta.items():
    genome_fasta[keys]=''.join(val)
nuc=open(args.bed,'r')
out=open(args.out+".fa",'w')
col_num=0
bed=nuc.readlines()
col=len(bed)
for lline in bed:
        col_num+=1
        chr_name=lline.rstrip().split()[0]
        start_end=lline.rstrip().split()[1:]
        leng=int(start_end[1])-int(start_end[0])
        out.write('>'+chr_name+':'+start_end[0]+'-'+start_end[1]+'\n'+genome_fasta[chr_name][int(start_end[0]):int(start_end[1])]+'\n')
out.close()

#Negative sequences consist of random shuffled positive sequences with random.shuffle
neg_fasta={}
out_neg=open(args.out+"_negtive.fa",'w')
for line in open(args.out+".fa",'r'):
    if line[0]=='>':
        seq_name=line.lstrip('>').strip()
        neg_fasta[seq_name]=[]
    else:
        neg_fasta[seq_name].append(line.strip())
for keys,val in neg_fasta.items():
    neg_fasta[keys]=''.join(val)
    fa=list(neg_fasta[keys])
    random.shuffle(fa)
    out_neg.write(">"+keys+"\n"+"".join(fa)+"\n")
out_neg.close()

#Construct a positive samples datasets
bed_dict_pos={}
pos_o=open(args.out+"pos.txt",'w')
for line in open(args.out+".fa",'r'):
    if line[0]==">":
       seq=line.strip()
       bed_dict_pos[seq]=[]
    else:
       bed_dict_pos[seq].append(line.strip())
for keys,val in bed_dict_pos.items():
    bed_dict_pos[keys]=''.join(val)
    pos_o.write('1'+'\t'+bed_dict_pos[keys]+'\n')
pos_o.close()

#Construct a negtive samples datasets
bed_dict_neg={}
neg_o=open(args.out+"neg.txt",'w')
for line in open(args.out+"_negtive.fa",'r'):
    if line[0]==">":
       seq=line.strip()
       bed_dict_neg[seq]=[]
    else:
       bed_dict_neg[seq].append(line.strip())
for keys,val in bed_dict_neg.items():
    bed_dict_neg[keys]=''.join(val)
    neg_o.write('0'+'\t'+bed_dict_neg[keys]+'\n')
neg_o.close()


#Using “one hot enconding” to preprocessing each sequence to the two-dimensional matrix of 4 columns. 
#Each base in the sequence is vectorized, convert A|a, C|c, G|g, T|t, N|n to: [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1], [0,0,0,0]

def load_data(filename):
    f=open(filename,'r')
    sequences=f.readlines()
    num=len(sequences)
    data=np.empty((num,1000,4),dtype='float32')
    label=np.empty((num,),dtype="int")
    for i in range(num):
        line=sequences[i].replace('\n','')
        list_line=re.split('\s+',line)
        one_sequence=list_line[1]
        for j in range(1000):
            if j<=len(one_sequence)-1:
                if re.findall(one_sequence[j],'A|a'):
                    data[i,j,:]=np.array([1.0,0.0,0.0,0.0],dtype='float32')
                if re.findall(one_sequence[j],'C|c'):
                    data[i,j,:]=np.array([0.0,1.0,0.0,0.0],dtype='float32')
                if re.findall(one_sequence[j],'G|g'):
                    data[i,j,:]=np.array([0.0,0.0,1.0,0.0],dtype='float32')
                if re.findall(one_sequence[j],'T|t'):
                    data[i,j,:]=np.array([0.0,0.0,0.0,1.0],dtype='float32')
                if re.findall(one_sequence[j],'N|n'):
                    data[i,j,:]=np.array([0.0,0.0,0.0,0.0],dtype='float32')
            else:
                data[i,j,:]=np.array([0.0,0.0,0.0,0.0],dtype='float32')
        label[i]=list_line[0]
    return data,label

pos_sample=args.out+"pos.txt"
neg_sample=args.out+"neg.txt"

data_pos,label_pos = load_data(pos_sample)
data_neg,label_neg = load_data(neg_sample)

#Divide postive datasets into training sets validate sets and test sets according to 60%, 20%and 20%

data_pos_train, data_pos_test, label_pos_train, label_pos_test = train_test_split(data_pos,label_pos, test_size=0.4, random_state=1)

data_pos_test, data_pos_val, label_pos_test, label_pos_val = train_test_split(data_pos_test, label_pos_test, test_size=0.5, random_state=1)


#Divide negtive datasets into training sets validate sets and test sets according to 60%, 20%and 20%

data_neg_train, data_neg_test, label_neg_train, label_neg_test = train_test_split(data_neg,label_neg, test_size=0.4, random_state=1)

data_neg_test, data_neg_val, label_neg_test, label_neg_val = train_test_split(data_neg_test, label_neg_test, test_size=0.5, random_state=1)

#Combined training sets
data_train = np.concatenate((data_pos_train,data_neg_train),axis=0)
label_train = np.concatenate((label_pos_train,label_neg_train),axis=0)
#Combined validate sets
data_val = np.concatenate((data_pos_val,data_neg_val),axis=0)
label_val = np.concatenate((label_pos_val,label_neg_val),axis=0)
#Combined test sets
data_test = np.concatenate((data_pos_test,data_neg_test),axis=0)
label_test = np.concatenate((label_pos_test,label_neg_test),axis=0)


#save
np.save('data_train.npy',data_train)
np.save('label_train.npy',label_train)
np.save('data_val.npy',data_val)
np.save('label_val.npy',label_val)
np.save('data_test.npy',data_test)
np.save('label_test.npy',label_test)


#Get training set sample sequence
sequence=[[] for i in range(data_train.shape[0])]
for i in range(data_train.shape[0]):
    for j in range(data_train.shape[1]):
        if (data_train[i,j,:] == np.array([1.0,0.0,0.0,0.0],dtype='float32')).all():
                 sequence[i]+='A'
        if (data_train[i,j,:] == np.array([0.0,1.0,0.0,0.0],dtype='float32')).all():                      sequence[i]+='C'
        if (data_train[i,j,:] == np.array([0.0,0.0,1.0,0.0],dtype='float32')).all(): 
                 sequence[i]+='G'
        if (data_train[i,j,:] == np.array([0.0,0.0,0.0,1.0],dtype='float32')).all():
                 sequence[i]+='T'
        if (data_train[i,j,:] == np.array([0.0,0.0,0.0,0.0],dtype='float32')).all():
                 sequence[i]+='N'

o=open(args.out+"train.txt",'w')
for i in range(data_train.shape[0]):    
   o.write(str(label_train[i])+'\t'+''.join(sequence[i])+'\n')
o.close()


