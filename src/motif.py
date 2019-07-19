'''
This script is for motif Visualization 
Author: Yin Shen
'''
#Required Modules
from __future__ import print_function
import os
import numpy as np
import pyfiglet
import keras
from keras.models import model_from_json
from keras import backend as K
import argparse
#specify which GPU(s) to be used
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


#Making large letters out of ordinary text with pyfiglet
ascii_banner = pyfiglet.figlet_format("charplant")
print(ascii_banner)

#Argument parsing
parser = argparse.ArgumentParser(description="motif Visualization ")
parser.add_argument("--nb_filter1","-n1",  default=200, type=int, required=False,
                    help="Number of filters in first layer of convolution.(default is 200)")
parser.add_argument("--filter_len1","-fl1",  default=19, type=int, required=False,
                    help="length of filters in first layer of convolution.(default is 19)")
parser.add_argument("--out", "-o", required=True,
                    help="prefix of the output file")
args = parser.parse_args()

get_input_file_path = os.chdir("../data_preprocessing")
input_file_path = os.getcwd()
input_file = os.listdir(input_file_path)
for file in input_file:
    if file[-9: ] == 'train.txt':
         motif_input_file = input_file_path+"/"+file

get_model_files_path = os.chdir("../model")
model_files_path = os.getcwd()
model_files = os.listdir(model_files_path)
for file in model_files:
     if file[-4: ] == 'json':
          model_architecture_path = model_files_path+"/"+file
     elif file[-2: ] =='h5':
          model_weights_path = model_files_path+"/"+file


get_current_path = os.chdir("../motif")
os.makedirs(args.out+"_motif")
filter_size=int(args.filter_len1)
model = model_from_json(open(model_architecture_path).read())
model.load_weights(model_weights_path)
f = K.function([model.layers[0].input,K.learning_phase()], [model.layers[1].output])


data=np.load("../data_preprocessing/data_train.npy")


def print_pwm(f, filter_idx, filter_pwm, nsites):
    if nsites < 10:
        return

    print('MOTIF filter%d' % filter_idx, end = "\n", file = f)
    print('letter-probability matrix: alength= 4 w= %d nsites= %d' % (filter_pwm.shape[0], nsites), end = "\n", file = f) 

    for i in range(0, filter_pwm.shape[0]):
        print('%.4f %.4f %.4f %.4f' % tuple(filter_pwm[i]), end = "\n", file = f)
    print('', end = '\n', file = f)



def logo_kmers(filter_outs,filter_size, seqs, filename, maxpct_t = 0.7):
    all_outs = np.ravel(filter_outs)
    all_outs_mean = all_outs.mean()
    all_outs_norm = all_outs - all_outs_mean
    raw_t = maxpct_t * all_outs_norm.max() + all_outs_mean

    with open(filename, 'w') as f:
        for i in range(filter_outs.shape[0]):
            for j in range(filter_outs.shape[1]):
                if filter_outs[i,j] > raw_t:
                    kmer = seqs[i][j-9:j+10]
                    if len(kmer) <filter_size:
                        continue
                    print('>%d_%d' % (i,j), end = '\n', file = f)
                    print(kmer, end = '\n', file = f)


def make_filter_pwm(filter_fasta):
    nts = {'A':0, 'C':1, 'G':2, 'T':3}
    pwm_counts = []
    nsites = 4
    for line in open(filter_fasta):
        if line[0] == '>':
            continue

        seq = line.rstrip()
        nsites += 1
        if len(pwm_counts) == 0:
            for i in range(len(seq)):
                pwm_counts.append(np.array([1.0]*4))

        for i in range(len(seq)):
            try:
                pwm_counts[i][nts[seq[i]]] += 1
            except KeyError:
                pwm_counts[i] += np.array([0.25]*4)

    pwm_freqs = []
    for i in range(len(pwm_counts)):
        pwm_freqs.append([pwm_counts[i][j]/float(nsites) for j in range(4)])

    return np.array(pwm_freqs), nsites - 4

def meme_header(f, seqs):
    nts = {'A':0, 'C':1, 'G':2, 'T':3}

    nt_counts = [1]*4
    for i in range(len(seqs)):
        for nt in seqs[i]:
            try:
                nt_counts[nts[nt]] += 1
            except KeyError:
                pass

    nt_sum = float(sum(nt_counts))
    nt_freqs = [nt_counts[i]/nt_sum for i in range(4)]

    print('MEME version 4', end = '\n', file = f)
    print('', end = '\n', file = f)
    print('ALPHABET= ACGT', end = '\n', file = f)
    print('', end = '\n', file = f)
    print('Background letter frequencies:', end = '\n', file = f)
    print('A %.4f C %.4f G %.4f T %.4f' % tuple(nt_freqs), end = '\n', file = f)
    print('', end = '\n', file = f)




sequence=[]
for line in open(motif_input_file,'r'):
    lines=line.strip().split('\t')
    one_sequence=lines[1]
    sequence.append(one_sequence)


y=0
final_output=np.empty([0,1000,int(args.nb_filter1)])
while y+128 <int(data.shape[0]):
   x=data[y:y+128]
   cnn_output=f([x])[0]
   y+=128
   final_output=np.concatenate([final_output,cnn_output],axis=0)
   print('%s/%s data points processed...' % (y, data.shape[0]))
x1=data[y:int(data.shape[0])]
cnn_output1=f([x1])[0]
final_output=np.concatenate([final_output,cnn_output1],axis=0)
print(final_output.shape)
cnn_layer_idx = 0
with open('%s/filter_meme.txt' % (args.out+"_motif"), 'w') as meme:
        meme_header(meme, sequence)
        for i in range(int(args.nb_filter1)):
            logo_kmers(final_output[:, :, i], filter_size,sequence, '%s/filter_%s.fa' % ((args.out+"_motif"), i))
            filter_pwm, nsites = make_filter_pwm('%s/filter_%s.fa' % ((args.out+"_motif"), i))
            print_pwm(meme, i, filter_pwm, nsites)
