from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
import pandas as pd
import numpy as np
import csv

#------------------ 데이터 로드
#----------------------------

okt = Okt()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
tokenizer = Tokenizer()
max_len = 30
X_train = []

#------------------------

#-------------------------------- 토큰화 리스트 csv 저장시작

print('파일열기시작')
f = open('/home/hanium/haniumapp/list_data.csv','r')
rdr = csv.reader(f)
for line in rdr:
    X_train.append(line)

f.close()

print('파일열기끝')
#--------------------------------- 토큰화 리스트 csv 저장 끝
#-------------------------------- 정수인코딩 시작
tokenizer.fit_on_texts(X_train)


threshold = 3
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value
# 전체 단어 개수 중 빈도수 2이하인 단어 개수는 제거.
# 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
vocab_size = total_cnt - rare_cnt + 2
tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
tokenizer.fit_on_texts(X_train)



X_train = tokenizer.texts_to_sequences(X_train)



#=================================정수인코딩 끝


#--------------------------- 감성분류 시작
loaded_model = load_model('/home/hanium/haniumapp/best_model.h5')

#--------------------------- 감성분류 끝


#---------------------------- 리뷰예측해보기
def sentiment_predict(new_sentence):
  new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
  print(new_sentence)
  new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
  print(new_sentence)
#  tokenizer.fit_on_texts(new_sentence)
#  print(tokenizer.fit_on_texts(new_sentence))
  encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
  print(encoded)
  pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
  print(pad_new)
  score = float(loaded_model.predict(pad_new)) # 예측
  if(score > 0.5):
    print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
    return score*100,1
  else:
    print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
    return ((1-score)*100),0


#sentiment_predict('재밌기도하고 슬프기도하지만 더 슬프네요 감동입니다')
