'''
This script is used for de novo prediction in the whole geneme

Author: Yin Shen
'''
#Required Modules
import pyfiglet
import argparse
import re
import os

#Making large letters out of ordinary text with pyfiglet
ascii_banner = pyfiglet.figlet_format("charplant")
print(ascii_banner)

#Argument parsing
parser = argparse.ArgumentParser(description='''De novo prediction''')
parser.add_argument("--genome", "-g", required=True,
                    help="genome file in fasta format")
parser.add_argument("--lines", "-l",default=20000, type=int, required=False,
                    help="The number of lines in a Sliding window cut genome file splited into smaller files (default is 20,000)")
parser.add_argument("--threshold", "-t",default=0.5, type=float, required=False,
                    help="the threshold adopted to assign positive predictions (default is 0.5)")
parser.add_argument("--out", "-o", required=True,    
                    help="prefix of the output file")  
args = parser.parse_args()



print("\033[1;30;34m%s\033[0m" %"Sliding window cutting genome...")
print("\033[1;30;34m%s\033[0m" %"please wait...")
fasta={}
for line in open(args.genome,'r'):
    if line[0]=='>':
        seq_name=line.lstrip('>').strip()
        fasta[seq_name]=[]
    else:
        fasta[seq_name].append(line.strip())
for keys,val in fasta.items():
    fasta[keys]=''.join(val)

o=open(args.out,'w')               
len_chrom={}
for key,val in fasta.items():
        len_chrom[key]=len(fasta[key])
        for i in range(0,len_chrom[key],1):
          if i+36<=int(len_chrom[key]):
             o.write(key+'\t'+str(i)+'\t'+str(i+36)+'\t'+fasta[key][i:i+36]+'\n')
          else:
             o.write(key+'\t'+str(i)+'\t'+str(len_chrom[key])+'\t'+fasta[key][i:len_chrom
[key]+1]+'\n')
             break
o.close()
print("\033[1;30;34m%s\033[0m" %"well done...")

print("\033[1;30;34m%s\033[0m" %"Split genome file according to multi-line...")
print("\033[1;30;34m%s\033[0m" %"please wait...")
splitLen = int(args.lines) 
output_prefix = args.out        # example: split_fasta_36_1_

input = open(args.out, 'r').read().split('\n')

counts = 1
for lines in range(0, len(input), splitLen):
    output_data = input[lines:lines+splitLen]
    output = open(output_prefix + str(counts), 'w')
    output.write('\n'.join(output_data))
    counts += 1
    output.close()
print("\033[1;30;34m%s\033[0m" %"well done...")

print("\033[1;30;34m%s\033[0m" %"batch write into python files...")
print("\033[1;30;34m%s\033[0m" %"please wait...")
get_model_files_path = os.chdir("../model")
model_files_path = os.getcwd()
model_files = os.listdir(model_files_path)
for file in model_files:
     if file[-4: ] == 'json':
          model_architecture_path = model_files_path+"/"+file
     elif file[-2: ] =='h5':
          model_weights_path = model_files_path+"/"+file

get_file_path = os.chdir("../de_novo_prediction")
file_path = os.getcwd()
files = os.listdir(file_path)
file_list=[]
for file in files:
    if file[-2: ] == 'py':
        continue 
    elif re.match(args.out+'\d+',file):
         file_list.append(file)

def tryint(s):            
    try:
        return int(s)
    except ValueError:
        return s
def str2int(v_str):    
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]
def sort_humanly(v_list):
    return sorted(v_list, key=str2int)

sort_file_list = sort_humanly(file_list)


python_file_1='''

def loading_data1(filename):
    f=open(filename,'r')
    sequences=f.readlines()
    num=len(sequences)
    data=np.empty((num,1000,4),dtype='float32')
    for i in range(num):
        line=sequences[i].replace("\\n",'')
        list_line=re.split('\s+',line)
        one_sequence=list_line[3]
        for j in range(1000):
            if j<=len(one_sequence)-1:
                if re.match(one_sequence[j],'A|a'):
                    data[i,j,:]=np.array([1.0,0.0,0.0,0.0],dtype='float32')
                if re.match(one_sequence[j],'C|c'):
                    data[i,j,:]=np.array([0.0,1.0,0.0,0.0],dtype='float32')
                if re.match(one_sequence[j],'G|g'):
                    data[i,j,:]=np.array([0.0,0.0,1.0,0.0],dtype='float32')
                if re.match(one_sequence[j],'T|t'):
                    data[i,j,:]=np.array([0.0,0.0,0.0,1.0],dtype='float32')
                if re.match(one_sequence[j],'N|n'):
                    data[i,j,:]=np.array([0.0,0.0,0.0,0.0],dtype='float32')
            else:
                data[i,j,:]=np.array([0.0,0.0,0.0,0.0],dtype='float32')
    return data
'''

python_file_2 = '''
result_new=np.empty((results.shape[0],1),dtype='int32')
for i in range(result_new.shape[0]):
         if results[i] >= %(threshold)s:
            result_new[i] = np.array([1], dtype='int32')
         else:
            result_new[i] = np.array([0], dtype = 'int32')
for i in result_new.tolist():
   o.write(str(i)+"\\n")    
o.close()
'''
for file in sort_file_list:
    file_read = open(file_path+"/"+file+'.py', 'w')
    file_read.write('import numpy as np'+'\n'+'import re'+'\n'+'from keras.models import model_from_json'+'\n'+"model = model_from_json(open('"+model_architecture_path+"').read())"+'\n'+"model.load_weights('"+model_weights_path+"')"+'\n'+python_file_1+'\n'+"data=loading_data1('"+file+"')"+'\n'+'results=model.predict_classes(data)'+'\n'+"o=open('whole_predict_fasta"+file+".txt','w')"+'\n'+python_file_2%dict(threshold=args.threshold)+'\n')    
    file_read.close()
print("\033[1;30;34m%s\033[0m" %"well done...")
