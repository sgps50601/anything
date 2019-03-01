from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.
def sayhello(request):
    return HttpResponse("hello我第一次玩這玩意")
def hello2(request,username):
    return HttpResponse("Hello"+username)
def hello3(request,username):
    now = datetime.now()
    return render(request,"hello3.html",locals())
def hello4(request,username):
    now = datetime.now()
    return render(request,"hello4.html",locals())
import random
def dice(request):
    no = random.randint(1000,2500)
    return render(request,"dice.html",{'no':no})