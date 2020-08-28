import tensorflow as tf
import pandas as pd
import numpy as np
import re 
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model #모델 저장하고 불러들이기
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint   
from konlpy.tag import Mecab
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

######데이터자료 시작

# 자료 가져오기  https://github.com/e9t/nsmc/   나중에는 직접 웹 크롤링으로 댓글을 가져와서 할 수 있었으면 좋겠다 !
#train_df = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt', sep =  '\t', quoting = 3))
#train_df = train_df.replace(np.nan, '', regex=True) 
train_df = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt', sep =   '\t', quoting = 3))
train_df = train_df.replace(np.nan, '', regex=True)  #regex 정규표현식 설정 

# 한글 제외한 다른 문자 모두 제거 
remove_except_ko = re.compile(r"^[가-힣ㄱ-ㅎㅏ-ㅣ\\s]")
#전처리 과정 함수화
def preprocess(text):
 text = re.sub(remove_except_ko, ' ',text).strip() #strip() 공백 지우기
 return text 
train_df['documet']=train_df['document'].map(lambda x : preprocess(x)) #mapping 해주기
#test_df['documet']=test_df['document'].map(lambda x : preprocess(x))

mecab = Mecab()
# Mecab 이용하여 토큰화, 한글자 제거, 불용어 제거 
stop_word = ['께서','에서', '이다','에게','으로', '이랑', '까지', '하다', '부터']
# 전처리 함수 만들기 -> 한글 제거하고 불용어 처리하기 
def postagging_mecab(text):
 text = mecab.morphs(text)
 text = [i for i in text if len(i) > 1] #한글자 제거 
 text = [i for i in text if i not in stop_word] #불용어 처리
 return(text)
# 토큰화 + 토큰 리스트 만들기
def make_tokens(df):
 df['tokens'] = '' #데이터 프레임에 tokens 자리 만들기
 tokens_list = [] #토큰 리스트 자리 만들기
 for i,row in df.iterrows(): #iterrows : 인덱스 판다스 1차원 데이터인 series로 만들어 접근
  if i%10000==0: #10000개씩 나누기 
   print(i, '/', len(df)) 
  token = postagging_mecab(df['documet'][i])
  tokens_list.append(token)
 return tokens_list,df 

#train_list, train_df = make_tokens(train_df)
train_list, train_df = make_tokens(train_df)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_list)


#단어를 숫자배열로 변환 
X_train_array_list = tokenizer.texts_to_sequences(train_list)
#X_test_array_list = tokenizer.texts_to_sequences(test_list)
X_train = X_train_array_list #다시 X_train 에 넣어주기 
#X_test = X_test_array_list #다시 X_text에 넣어주기 

# 레이블링 데이터 행렬변환
Y_train = np.array(train_df['label'])
#Y_test = np.array(test_df['label'])


max_len = 30
X_train = pad_sequences(X_train, maxlen = max_len) #패딩 해준 값 다시 X_train에 넣기 
#X_test = pad_sequences(X_test, maxlen = max_len) 

#데이터자료 종료



vocab_size = len(X_train) # X_train의 개수 
# 신경망 층, 레이어 쌓아주기
# 모델 설정하고 실행하는 부분 
model = Sequential() #케라스는 층을 조합하여 모델을 만든다 -> 즉, 모델은 층의 그래프라고 보면 된다
# model.add(...) 는 층을 추가하는 것을 의미함
model.add(Embedding(vocab_size, 100)) #층을 형성
model.add(LSTM(128))
model.add(Dense(128, activation='relu')) # 첫번째 층 
model.add(Dense(1, activation='sigmoid')) # 두번째 층

# 검증 데이터 손실(val_loss)이 증가하면, 과적합이 될수 있기 때문에 검증 데이터 손실이 4회 증가하면 학습을 조기 종료(Early Stopping). 
# ModelCheckpoint를 사용하여 검증 데이터의 정확도(val_acc)가 이전보다 좋아질 경우에만 모델을 저장
#es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
#mc = ModelCheckpoint('review_data.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

#model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])              # 모델 학습시키기

loaded_model = load_model('review_data.h5') #정확도가 가장 높았을 때 저장된 모델을 로드

def predict_pos_text(text):
 token=[]
 tokens = postagging_mecab(text) 
 token.append(tokens)
 print(token) #새로 들어온 텍스트 토큰화 
 X_train_arrary_list = tokenizer.texts_to_sequences(token) #정수 인코딩 . 단어를 숫자배열로 변환
 max_len=30 # 패딩
 X_train = pad_sequences(X_train_arrary_list, maxlen = max_len) 
 score = float(loaded_model.predict(X_train)) # 점수 예측 
 print('score:', type(score))
 if score>0.5:
  print("[{}]는 {:.2f}% 확률로 긍정 리뷰입니다.\n".format(text, score * 100))
 else:
  print("[{}]는 {:.2f}% 확률로 부정 리뷰입니다.\n".format(text, (1 - score) * 100))


# 검증하기
predict_pos_text('3D만 아니었어도 별 다섯 개 줬을텐데.. 왜 3D로 나와서 제 심기를 불편하게 하죠??')
predict_pos_text('너무 재미있었습니다. 한번 더 보고 싶네요. 기분좋았습니다')
predict_pos_text('재미있는지 잘 모르겠어요. 가끔 재밌기도하고 재미없기도하고 슬프기도하고 우울하기도하고 긍정적이긴하네요')

