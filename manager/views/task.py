import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from manager.models import Task
from manager.utils.BootStrap import BootStrapModelForm
from manager.utils.Pagination import Pagination

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
        }


@csrf_exempt
def task_list(request):
    queryset = Task.objects.all().order_by('-id')
    form = TaskModelForm()
    page_object = Pagination(request,queryset,page_size=5)
    context = {
        "queryset":page_object.page_queryset,
        "form":form,
        "page_string":page_object.html()
    }
    return render(request, 'task_list.html', context)


@csrf_exempt
def task_ajax(request):
    print('get请求:', request.GET)
    print('post请求:', request.POST)
    data_dict = {
        "status": True,
        "data": [11, 22, 33]
    }
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    print(request.POST)

    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict))
