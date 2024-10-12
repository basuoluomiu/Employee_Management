from django.shortcuts import render
from django.http import JsonResponse

def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    return render(request,'chart_new.html')
