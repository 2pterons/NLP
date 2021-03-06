# -*- coding: utf-8 -*-
"""2-4.keras_tokenizer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1shDHzOOwgZK9UphApOfRWH0kPNDuaYPN
"""

import numpy as np
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
nltk.download('punkt')
nltk.download('stopwords')  # 불용어 목록

nltk.download('gutenberg')
text_id = nltk.corpus.gutenberg.fileids()
text_id

# 특정 파일의 텍스트 문서를 조회한다.
text = nltk.corpus.gutenberg.raw('austen-emma.txt')
print(text[:600])
print("문자 개수 = ", len(text))

sentences = nltk.sent_tokenize(text)
sentences[:5]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)

# 단어사전
word2idx = tokenizer.word_index
idx2word = {v:k for k, v in word2idx.items()}

# 문장을 단어의 인덱스로 표현
sent_idx = tokenizer.texts_to_sequences(sentences)
sent_idx[0]

# 문장을 이진 행렬 형태로 표시한다. 1은 사전에 사용된 단어임을 의미한다.
sent_bow = tokenizer.texts_to_matrix(sentences, mode='binary')
print(sent_bow[0])

# 확인
np.where(sent_bow[0] == 1)
set(sent_idx[0])

