from django.shortcuts import render
from rest_framework.views import APIView



def get(request):
    return render(request,'index.html')

def main(request):
    return render(request,'main.html')

def mystock(request):
    return render(request, 'mystock.html')

def favorite(request):
    return render(request, 'favorite.html')

def nowstock(request):
    return render(request, 'nowstock.html')

def order(request):
    return render(request,'order.html')

def profit(request):
    return render(request,'profit.html')

def stockindex(request):
    return render(request,'stockindex.html')