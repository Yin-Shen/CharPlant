'''
This script is training cnn model for charplant.

Author: Yin Shen
'''
#Required Modules
import sys
import argparse
import time
import numpy as np
import re
import pyfiglet
from keras.models import Sequential,model_from_json
from keras.callbacks import ModelCheckpoint,EarlyStopping 
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.pooling import GlobalMaxPooling1D
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras import regularizers
from keras.optimizers import SGD
from sklearn.metrics import roc_curve, auc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#specify which GPU(s) to be used
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

np.random.seed(666)

#Making large letters out of ordinary text with pyfiglet
ascii_banner = pyfiglet.figlet_format("charplant")
print(ascii_banner)

#Argument parsing
parser = argparse.ArgumentParser(description="Training Charplant cnn model")
parser.add_argument("--epochs", "-e", default=150, type=int, required=False,
                    help="Number of epochs.(default is 150)")
parser.add_argument("--patience", "-p", default=20, type=int, required=False,
                    help='Number of epochs  for early stopping.(default is 20)')
parser.add_argument("--learningrate", "-lr", default=0.001, type=float, required=False,
                   help='Learning rate.(default is 0.001)')
parser.add_argument("--batch_size","-b",  default=128, type=int, required=False,	
                    help="Batch Size.(default is 128)")
parser.add_argument("--dropout","-d",  default=0.6, type=float,required=False,
                    help="Dropout rate.(default is 0.6)")
parser.add_argument("--nb_filter1","-n1",  default=200, type=int, required=False,
                    help="Number of filters in first layer of convolution.(default is 200)")
parser.add_argument("--nb_filter2","-n2",  default=100, type=int, required=False,
                    help="Number of filters in second layer of convolution.(default is 100)")
parser.add_argument("--filter_len1","-fl1",  default=19, type=int, required=False,
                    help="length of filters in first layer of convolution.(default is 19)")
parser.add_argument("--filter_len2","-fl2",  default=11, type=int, required=False,
                    help="length of filters in second layer of convolution.(default is 11)")
parser.add_argument("--hidden","-hd", default=200, type=int, required=False,
                    help="units in the fully connected layer.(default is 200)")
args = parser.parse_args()



print("\033[1;30;34m%s\033[0m" %"loading data...")
print("\033[1;30;34m%s\033[0m" %"please wait...")
sys.stdout.flush()

data_train=np.load('../data_preprocessing/data_train.npy')
label_train=np.load('../data_preprocessing/label_train.npy')
data_val=np.load('../data_preprocessing/data_val.npy')
label_val=np.load('../data_preprocessing/label_val.npy')
data_test=np.load('../data_preprocessing/data_test.npy')
label_test=np.load('../data_preprocessing/label_test.npy')
print("\033[1;30;34m%s\033[0m" %"well done...")

model=Sequential()
model.add(Convolution1D(int(args.nb_filter1),
                        int(args.filter_len1),
                        border_mode='same',
                        input_shape=(1000,4)))
model.add(Activation('relu'))
model.add(Dropout(float(args.dropout)))

model.add(Convolution1D(int(args.nb_filter2),
                        int(args.filter_len2),
                        border_mode='same'))
model.add(Activation('relu'))
model.add(Dropout(float(args.dropout)))


model.add(Flatten())
model.add(Dense(int(args.hidden),init='normal',activation='relu'))
model.add(Dropout(float(args.dropout)))

model.add(Dense(1,init='normal',activation='linear'))
model.add(Activation('sigmoid'))

sgd=SGD(lr=float(args.learningrate),decay=1e-5,momentum=0.9,nesterov=True)

print("\033[1;30;34m%s\033[0m" %"model compiling...")
print("\033[1;30;34m%s\033[0m" %"please wait...")
sys.stdout.flush()
model.compile(loss='binary_crossentropy',optimizer=sgd,metrics=['accuracy'])  
early_stopping =EarlyStopping(monitor='val_loss', patience=args.patience,verbose=1)
checkpointer = ModelCheckpoint(filepath='model_weights'+str(args.nb_filter1)+'-'+str(args.nb_filter2)+'-'+str(args.filter_len1)+'-'+str(args.filter_len2)+'-'+str(args.hidden)+'-'+str(args.dropout)+'-'+str(args.learningrate)+'-'+str(args.batch_size)+'-'+str(args.epochs)+'-'+str(args.patience)+'.h5', verbose=1, save_best_only=True)
print("\033[1;30;34m%s\033[0m" %"well done...")

print("\033[1;30;34m%s\033[0m" %"training...")
print("\033[1;30;34m%s\033[0m" %"please wait...")
time_start = time.time()
result=model.fit(data_train,label_train,batch_size=args.batch_size,nb_epoch=args.epochs,shuffle=True,validation_data=(data_val,label_val),callbacks=[checkpointer, early_stopping])
time_end = time.time()
print("\033[1;30;34m%s\033[0m" %"well done...")

json_string=model.to_json()
open('model_architecture'+str(args.nb_filter1)+'-'+str(args.nb_filter2)+'-'+str(args.filter_len1)+'-'+str(args.filter_len2)+'-'+str(args.hidden)+'-'+str(args.dropout)+'-'+str(args.learningrate)+'-'+str(args.batch_size)+'-'+str(args.epochs)+'-'+str(args.patience)+'.json','w').write(json_string)

model.load_weights('model_weights'+str(args.nb_filter1)+'-'+str(args.nb_filter2)+'-'+str(args.filter_len1)+'-'+str(args.filter_len2)+'-'+str(args.hidden)+'-'+str(args.dropout)+'-'+str(args.learningrate)+'-'+str(args.batch_size)+'-'+str(args.epochs)+'-'+str(args.patience)+'.h5')
score = model.evaluate(data_val,label_val, verbose=0)
print('accuracy_validate :',score[1])

score1 = model.evaluate(data_test,label_test, verbose=0)
print('Test loss:', score1[0])
print('Test accuracy:', score1[1])


print('training time : %d sec' % (time_end-time_start))


pred=model.predict_proba(data_test)

fpr, tpr, thresholds = roc_curve(label_test, pred)
roc_auc = auc(fpr, tpr)
print('the auc is ',roc_auc)


print("\033[1;30;34m%s\033[0m" %"plot ROC curve...")

plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.savefig('pictureauc'+str(args.nb_filter1)+'-'+str(args.nb_filter2)+'-'+str(args.filter_len1)+'-'+str(args.filter_len2)+'-'+str(args.hidden)+'-'+str(args.dropout)+'-'+str(args.learningrate)+'-'+str(args.batch_size)+'-'+str(args.epochs)+'-'+str(args.patience)+'.png')
plt.close()


print("\033[1;30;34m%s\033[0m" %"plot figure...")


plt.plot(result.history['loss'])
plt.plot(result.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('pictureloss'+str(args.nb_filter1)+'-'+str(args.nb_filter2)+'-'+str(args.filter_len1)+'-'+str(args.filter_len2)+'-'+str(args.hidden)+'-'+str(args.dropout)+'-'+str(args.learningrate)+'-'+str(args.batch_size)+'-'+str(args.epochs)+'-'+str(args.patience)+'.png')
plt.close()

plt.figure
plt.plot(result.epoch,result.history['acc'],label="acc")
plt.plot(result.epoch,result.history['val_acc'],label="val_acc")
plt.scatter(result.epoch,result.history['acc'],marker='*')
plt.scatter(result.epoch,result.history['val_acc'])
plt.legend(loc='under right')
plt.savefig('picture'+str(args.nb_filter1)+'-'+str(args.nb_filter2)+'-'+str(args.filter_len1)+'-'+str(args.filter_len2)+'-'+str(args.hidden)+'-'+str(args.dropout)+'-'+str(args.learningrate)+'-'+str(args.batch_size)+'-'+str(args.epochs)+'-'+str(args.patience)+'.png')
plt.close()
