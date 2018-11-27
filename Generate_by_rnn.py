#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy,sys,time
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import string


# In[2]:


filename = 'data.tsv'
raw_text=open(filename,'r').read().lower()


# In[3]:


raw_text = raw_text.replace('<br>', ' ')
processed_text = raw_text.replace('\n', ' ')
raw_text = ''.join([c for c in raw_text if not c in string.punctuation])
processed_text = ''.join([c for c in processed_text if not c in string.punctuation])
words=sorted(list(set(processed_text.split(' '))))


# In[4]:


word_to_int = dict((c,i) for i, c in enumerate(words))


# In[ ]:





# In[5]:


n_words = len(processed_text.split(' '))
n_vocab = len(words)


# In[6]:


seq_length = 5
lines = raw_text.split('\n')
dataX = []
dataY = []
for haiku in lines:
    haiku_list = haiku.split(' ')
    haiku_list = [h for h in haiku_list if h != '']
    for i in range(0, len(haiku_list)-1-seq_length):
        seq_in=haiku_list[i:i+seq_length]
        seq_out=haiku_list[i+seq_length]
        dataX.append([word_to_int[w] for w in seq_in])
        dataY.append(word_to_int[seq_out])


# In[7]:


n_patterns = len(dataX)
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
X = X/float(n_vocab)
y = np_utils.to_categorical(dataY)


# In[8]:


X[0]


# In[10]:


print(word_to_int['cant']/n_vocab)
print(word_to_int['you']/n_vocab)
print(word_to_int['see']/n_vocab)
print(word_to_int['how']/n_vocab)
print(word_to_int['much']/n_vocab)


# In[13]:


model = Sequential()
# model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(256,input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(256,input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
# model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')


# In[14]:


model.fit(X, y, epochs=1, batch_size=2000)


# In[ ]:


int_to_word=dict((i,c) for i,c in enumerate(words))


# In[ ]:


numpy.random.seed(int(time.time()))
start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print('pattern is', pattern)

sys.stdout.write("Generated Haiku: ")
generated=' '.join([int_to_word[value] for value in pattern])
for i in range(10):
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = ' ' + int_to_word[index] 
    #seq_in = [int_to_word[value] for value in pattern]
    #sys.stdout.write(result)
    generated+=result
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
sys.stdout.write("%s\n"%generated)


# In[ ]:





# In[ ]:





# In[ ]:




