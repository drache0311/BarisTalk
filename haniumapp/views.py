from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
#csrf 예외를 위해 import
from django.views.decorators.csrf import csrf_exempt
# nlp 폴더의 nlp.py(문장 감성분석 %수치 소스)를 import
import sys
sys.path.append('home/hanium/haniumapp')
from . import nlp

# 변수 선언

#score = 0	# 긍정부정 점수를 담는 변수
#flag = 0	# 긍정이면 1, 부정이면 0
sum = 0		# 최종값 점수를 담는 변수


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
        if action == 'start':
#            return start(params)
            return start(queryText)
        elif action == 'chatting':
            return chatting(queryText)
        elif action == 'stop':
            return stop(params)
        elif action is None:
            return check(queryText)

# intent Name 에 따른 기능

def start(queryText):

    #text,score = naverNlp.predict_pos_text('3D만 아니었어도 별 다섯 개 줬을텐데.. 왜 3D로 나와서 제 심기를 불편하게 하죠??')
    # JSON 형식의 response 입니다.


    global sum
    #score는몇%인지 , flag는1이면 긍정,0이면 부정
    score,flag =  nlp.sentiment_predict(queryText)

    # 채탱끝 이라고 오면 채팅종료
    # sum 값을 0으로 초기화 하고 채팅종료 response를 보낸다.
    if(queryText == '채팅끝'):

        # 점수(sum)가 -40이하
        if(sum<-40):
            response = {
                'fulfillmentText' : '당신은 매우 힘드시군요! \n 그럴떈 차가운 아메리카노는 어떠신가요?'
            }
            sum = 0
            return JsonResponse(response, safe=False)
        # 점수(sum)가 -20이하~ -40
        elif(sum<-20):
            response = {
                'fulfillmentText' : '기분이 별로인가요?! \n 기분전환으로 카페모카는 어떠신가요?'
            }
            sum = 0
            return JsonResponse(response, safe=False)
        # 점수(sum)가 0이하 ~ -20
        elif(sum<0):
            response = {
                'fulfillmentText' : '평범한 일상인가요?! \n 콜드브류를 더해보세요!'
            }
            sum = 0
            return JsonResponse(response, safe=False)
        # 점수(sum)가 20이하 ~ 0
        elif(sum<20):
            response = {
                'fulfillmentText' : '좋은일이 있으시나요?! \n 바닐라라뗴로 더욱 즐겨보세요!'
            }
            sum = 0
            return JsonResponse(response, safe=False)
        # 점수(sum)가 20이상
        else:
            response = {
                'fulfillmentText' : '최고의 날이네요! \n 아이스 아메리카노로 식혀보세요'
            }
            sum = 0
            return JsonResponse(response, safe=False)


    # 채팅끝이 아니면 분석시작
    else:
        # 긍정이면 score를 sum에 더하고 부정이면 sum에 뺀다.
        if(flag == 1):
            sum+=int(score)
        elif(flag == 0):
            sum-=int(score)

        response = {
            'fulfillmentText' : '계속 이야기 해주세요'
        }

        return JsonResponse(response, safe=False)




