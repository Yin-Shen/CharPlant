'''
This script is used for de novo prediction in the whole geneme

Get positive sample from de novo prediction
Author: Yin Shen
'''
#Required Modules
import pyfiglet
import argparse
import os
#Making large letters out of ordinary text with pyfiglet
ascii_banner = pyfiglet.figlet_format("charplant")
print(ascii_banner)
#Argument parsing
parser = argparse.ArgumentParser(description="motif Visualization ")
parser.add_argument("--input", "-i", required=True,
                    help="The prediction  output file generated by this de_novo_prediction(example :split_fasta_36_5)")
parser.add_argument("--name", "-n", required=True,
                    help="The name of the species")
args = parser.parse_args()


get_input_file_path = os.chdir("de_novo_prediction/")
input_file_path = os.getcwd()
input_file = os.listdir(input_file_path)

for file in input_file:
    if file[-17: ] == args.input:
         input_files = input_file_path+"/"+file
#Get positive sample
genome=[]
genome_line=0
for l in open(input_files,'r'):
    ll=l.strip()
    genome.append(ll)
    genome_line +=1 

predict=[]
for line in open('whole_predict','r'):
    lines=line.strip()
    liness=lines.lstrip('[').rstrip(']')
    predict.append(liness)


genome_pre={}
lines=0
while lines < genome_line:
    k_name=genome[lines]
    genome_pre[k_name]=predict[lines]
    lines+=1

o=open('whole_pre.txt','w')
for k,v in genome_pre.items():
    if genome_pre[k] == '1':
        kk=k.strip().split('\t')
        o.write(kk[3]+'\n')
o.close()

#construct fasta file
i=0
o=open('whole_pre.fa','w')
for line in open('whole_pre.txt','r'):
   lines=line.strip()
   o.write('>'+args.name+'-'+'predict_region'+str(i)+'\n'+lines+'\n')
   i+=1
o.close()
print("\033[1;30;34m%s\033[0m" %"Done...")
