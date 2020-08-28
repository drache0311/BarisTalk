from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
#csrf 예외를 위해 import
from django.views.decorators.csrf import csrf_exempt
# nlp 폴더의 nlp.py(문장 감성분석 %수치 소스)를 import
import sys
sys.path.append('home/hanium/haniumapp')
from . import nlp



# Create your views here.

def index(request):
    return render(request, 'index.html')


def chat(request):
    return render(request, 'chat.html')

def cafe(request):
    return render(request, 'cafe.html')


# 웹훅 서비스
@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        req = json.loads(request.body)

        #request의 action을 파악합니다.
        action = req.get('queryResult').get('action')

        #params를 획득합니다.
        params = req.get('queryResult').get('parameters')

        #queryText를 획득합니다.
        queryText = req.get('queryResult').get('queryText')

        # action에 따라서 이동합니다.
        if action == 'welcome':
#            return welcome(params)
            return welcome(queryText)

# intent Name 에 따른 기능

def welcome(queryText):

    #text,score = naverNlp.predict_pos_text('3D만 아니었어도 별 다섯 개 줬을텐데.. 왜 3D로 나와서 제 심기를 불편하게 하죠??')
    # JSON 형식의 response 입니다.

    #text는몇%인지 , flag는1이면 긍정,0이면 부정
    score,flag =  nlp.sentiment_predict(queryText) 
    response = {
#        'fulfillmentText' : '반갑습니다 웹훅성공 !! DT.'
        'fulfillmentText' : score

    }

    return JsonResponse(response, safe=False)
