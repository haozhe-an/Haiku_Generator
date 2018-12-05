import numpy,sys,time
# import gensim
import string
import gensim
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from gensim.models import Word2Vec
from gensim import corpora
from gensim.models import Word2Vec
from gensim.test.utils import common_texts, get_tmpfile

input_line=[]
size = len(sys.argv)-1
a=0
for argument in sys.argv:
    if a==0:
        a=a+1
        continue
    input_line.append(argument)
print(input_line)
similarity_time = 0
similarity_game = 0
similarity_life = 0
similarity_money = 0
similarity_person = 0
model = Word2Vec.load("model/word2vec.model")


for word in input_line:
    similarity_time += model.similarity(word, 'time')
    similarity_game += model.similarity(word, 'game')
    similarity_life += model.similarity(word, 'life')
    similarity_money += model.similarity(word, 'money')
    similarity_person += model.similarity(word, 'person')
result = max([similarity_time,similarity_game,similarity_life,similarity_money,similarity_person])
if result == similarity_time:
    model = Word2Vec.load("time_model/word2vec.model")
elif result == similarity_game:
    model = Word2Vec.load("game_model/word2vec.model")
elif result == similarity_life:
    model = Word2Vec.load("life_model/word2vec.model")
elif result == similarity_money:
    model = Word2Vec.load("money_model/word2vec.model")
else:
    model = Word2Vec.load("person_model/word2vec.model")
