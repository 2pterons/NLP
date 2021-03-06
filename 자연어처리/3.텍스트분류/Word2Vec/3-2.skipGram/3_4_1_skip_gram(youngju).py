# -*- coding: utf-8 -*-
"""3-4-1_skip_gram(youngju).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZoCWIuv_pnyVdS5mB2sj9BaGfhYU-kKK
"""

# -*- coding: utf-8 -*-
"""210706(skip_gram).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JpcWJ2m2mYZncw51w2L9XaUIisN8ch1Y
"""

import nltk
nltk.download('punkt')
nltk.download('gutenberg')
nltk.download('averaged_perceptron_tagger')

nltk.download('stopwords')  # 불용어 목록
stopwords = nltk.corpus.stopwords.words('english')  # 등록된 stop word
stopwords.extend([',','.','[',']',';'])

text_id = nltk.corpus.gutenberg.fileids()

from nltk.stem import PorterStemmer
porter = PorterStemmer()

word2idx = {}

# 영문 소설 10개만 사용한다.
n = 10
sent =[]
cnt = 0
for i, text_id in enumerate(nltk.corpus.gutenberg.fileids()[:n]):
    text = nltk.corpus.gutenberg.raw(text_id)
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        word_tok = nltk.word_tokenize(sentence)
        sent_nnjj = [word for word, pos in nltk.pos_tag(word_tok) if pos == 'NN' or pos == 'JJ' or pos=='VB']
        clean_tok = []
        for word in sent_nnjj:
          if word.lower() not in stopwords:
            # clean tok 생성
            #stem_word = porter.stem(word)
            stem_word = word.lower()
            clean_tok.append(stem_word)
            # word2idx 생성 만약 딕셔너리에 단어가 없다면
            if word2idx.get(stem_word) == None:
              word2idx[stem_word] = cnt
              cnt+=1
        sent.append(clean_tok)
    print('{}: {} ----- processed.'.format(i+1, text_id))

idx2word = {v:k for k, v in word2idx.items()}

print("총 문장 개수 =", len(sent))
print(sent[0])

train_x =[]
train_y = []
for sentence in sent:
  tri_grams = nltk.trigrams(sentence)
  try:
    for left, center, right in tri_grams:
      train_x.append(word2idx[center])
      train_y.append(word2idx[left])
      train_x.append(word2idx[center])
      train_y.append(word2idx[right])
  except:
    continue

len(train_x)

len(train_y)

len(word2idx)

from tensorflow.keras.layers import Input, Dense, Dropout, Embedding
from tensorflow.keras.layers import Flatten, Dot, Activation
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import numpy as np
from sklearn.model_selection import train_test_split

train_x = np.array(train_x)
train_y = np.array(train_y)

train_x.shape

train_y.shape

#x_train, x_test, y_train, y_test = train_test_split(train_x, train_y, test_size=0.2)

n_factors = 32

x_input = Input(batch_shape = (None, 1))
x_emb = Embedding(input_dim = len(word2idx)+1, output_dim = n_factors)(x_input)
y_output = Dense(len(word2idx)+1, activation='softmax')(x_emb)

model = Model(x_input, y_output)
model.compile(loss='SparseCategoricalCrossentropy', optimizer = Adam(learning_rate=0.01), metrics=['sparse_categorical_accuracy'])
model.summary()

train_x.max()

# 학습
hist = model.fit(train_x, train_y, 
                 batch_size=4096, 
                 epochs = 30,
                 )

import matplotlib.pyplot as plt

plt.plot(hist.history['loss'], label='train')
plt.legend()
plt.show()

for i in range(0,200,2):
  print("train_x:", idx2word[train_x[i]], " train_y: ", idx2word[train_y[i]], "pred_y: ", 
        idx2word[np.argmax(model.predict(np.array([train_x[i]])).flatten() )])

a = 'friend'
b= 'strong'

vector_a = model.predict(np.array([word2idx[a]]))
vector_b = model.predict(np.array([word2idx[b]]))
sum_vector = vector_a+vector_b
sub_vector = vector_a-vector_b

print("sum_vector: ",idx2word[np.argmax(sum_vector)])
print("sub_vector: ",idx2word[np.argmax(sub_vector)])