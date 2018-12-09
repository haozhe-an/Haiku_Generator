#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy,sys,time
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import string
import gensim
from gensim.models import Word2Vec
import requests
from bs4 import BeautifulSoup
import numpy as np


# In[2]:


def read_input(filename):
    processed_text = ''
    doc = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            line = line.lower()
            line = line.replace('<br>', ' ')
            line = line.replace('\n', ' ')
            line = ''.join([c for c in line if not c in string.punctuation])
            doc.append([w for w in line.split(' ') if not w == ''])
            processed_text += line
            
    words=sorted(list(set(processed_text.split(' '))))
    word_to_int = dict((c,i) for i, c in enumerate(words))
    int_to_word=dict((i,c) for i,c in enumerate(words))   
    return doc, word_to_int, int_to_word

def find_rhymes(word):
    url = 'http://rhymebrain.com/en/What_rhymes_with_' + word + '.html'
    body = requests.get(url).text
    soup = BeautifulSoup(body, 'lxml')
    
    res = str(soup.find_all(attrs={'class':'wordpanel'}))
    res = [x for x in res.split('>') if x.find('wordpanel') == -1]
    res = [x.split('<')[0].strip() for x in res if x != "]"]
    return res

def count_word_syllables(word):
    word = word.lower()
    # Count the syllables in the word.
    syllables = 0
    for i in range(len(word)) :
    # If the first letter in the word is a vowel then it is a syllable.
        if i == 0 and word[i] in "aeiouy" :
            syllables = syllables + 1
    # Else if the previous letter is not a vowel.
        elif word[i - 1] not in "aeiouy" :
      # If it is no the last letter in the word and it is a vowel.
            if i < len(word) - 1 and word[i] in "aeiouy" :
                syllables = syllables + 1
      # Else if it is the last letter and it is a vowel that is not e.
            elif i == len(word) - 1 and word[i] in "aiouy" :
                syllables = syllables + 1
    # Adjust syllables from 0 to 1.
    if len(word) > 0 and syllables == 0 :
        syllables == 0
        syllables = 1
    return syllables

def count_syllables(sentence):
    words = sentence.split(' ')
    count = 0
    for w in words:
        count += count_word_syllables(w)
    return count


# In[3]:


# train word2vec
filename = 'time.tsv'
doc, word_to_int, int_to_word = read_input(filename)
# build vocabulary and train model
doc_list = [d for d in doc]
model = gensim.models.Word2Vec(
        doc_list,
        size=150,
        window=10,
        min_count=1,
        workers=10)
model.train(doc_list, total_examples=len(doc_list), epochs=10)


# In[4]:


seq_length = 5
dataX = []
dataY = []
for haiku_list in doc_list:
    for i in range(0, len(haiku_list)-1-seq_length):
        seq_in=haiku_list[i:i+seq_length]
        seq_out=haiku_list[i+seq_length]
        dataX.append([model.wv[w] for w in seq_in])
        #dataY.append(model.wv[seq_out])
        dataY.append(word_to_int[seq_out])
        
n_patterns = len(dataX)
X = numpy.reshape(dataX, (n_patterns, seq_length, len(dataX[0][0])))
#y = numpy.array(dataY)
y = np_utils.to_categorical(dataY)


# In[5]:


rnn_time = Sequential()
rnn_time.add(LSTM(512, input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
rnn_time.add(Dropout(0.2))
rnn_time.add(LSTM(512, input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
rnn_time.add(Dropout(0.5))
rnn_time.add(Flatten())
rnn_time.add(Dense(y.shape[1], activation='softmax'))
rnn_time.compile(loss='categorical_crossentropy', optimizer='adam')


# In[8]:


rnn_time.fit(X, y, epochs=100, batch_size=256)


# In[24]:


input_words = 'Singing in the rain is'
input_words = input_words.lower()
input_words = input_words.split(' ')
pattern = [model.wv[w] for w in input_words]
words = ''
syllables_count = 0
for p in pattern:
    word = [w for w, i in model.wv.most_similar(positive=[p], topn=1)]
    words += word[0] + ' '
    syllables_count += count_syllables(word[0])

print('Pattern is:', words)

last_word = words.split()[-1]

sys.stdout.write("Generated Haiku: ")
generated=''.join(words)

complete = False
for i in range(20):
    if complete:
        break
    x = numpy.reshape(pattern, (1, seq_length, len(dataX[0][0])))
    prediction = rnn_time.predict(x, verbose=0)
    index = numpy.argmax(prediction[0])
    result = int_to_word[index] + ' '
    num_syllables = count_syllables(result)
    pred = prediction[0]
    while syllables_count + num_syllables > 17:
        pred[index] = float('-inf')
        index = numpy.argmax(pred)
        if index == 0:
            continue
        result = int_to_word[index] + ' '
        num_syllables = count_syllables(result)

    syllables_count += num_syllables
    if syllables_count == 17:
        complete = True
        
        ############ rhyme ##############
        rhyme_candidates = find_rhymes(last_word)
        last_word_syllables = count_syllables(result)
        replace_candidates = []
        highest_score = 0
        # the last word to 'replace' with
        temp = result.strip()
        print("initial predicion:", result)
        #print("last word: ", last_word)
        for r in rhyme_candidates:
            if count_syllables(r) == last_word_syllables:
                replace_candidates.append(r)
                
        all_vocabs_list = list(model.wv.vocab.keys())
        #print(replace_candidates)
        for r in replace_candidates:
            if r in all_vocabs_list:
                #print(r)
                score = model.wv.similarity(temp, r)
                if score > highest_score:
                    highest_score = score
                    #print("score: ", score)
                    result = r        
        
    generated+=result
    pattern.append(model.wv[result.strip()])
    pattern = pattern[1:len(pattern)]
sys.stdout.write("%s\n"%generated)


# In[13]:


rnn_time.save_weights("model_time.h5")
with open('model_time_architecture.json', 'w') as f:
    f.write(rnn_time.to_json())


# In[14]:


rnn_time.save("model_time_whole.h5")


# In[ ]:




