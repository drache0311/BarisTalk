"""hanium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import haniumapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', haniumapp.views.index, name='index'),
        # 맨앞' '은 주소 뒤 아무것도 입력안했을시를 의미
        # 중간views.index는 views.py의 index함수의미
    path('chat/', haniumapp.views.chat, name='chat'),
    path('webhook/', haniumapp.views.webhook, name='webhook'),
]
