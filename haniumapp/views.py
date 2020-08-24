from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
#csrf 예외를 위해 import
from django.views.decorators.csrf import csrf_exempt


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

        # action에 따라서 이동합니다.
        if action == 'welcome':
            return welcome()


# intent Name 에 따른 기능

def welcome():
    # JSON 형식의 response 입니다.
    response = {
        'fulfillmentText' : '반갑습니다 웹훅성공 !! DT.'
    }

    return JsonResponse(response, safe=False)
