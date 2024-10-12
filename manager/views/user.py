from django.shortcuts import render,redirect
from manager import models
from manager.models import Userinfo
from manager.utils.Pagination import Pagination
from manager.utils.BootStrap import BootStrapModelForm


def user_list(request):
    # 用户列表
    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict["listname__contains"] = search_data
    queryset = Userinfo.objects.filter(**data_dict)


    page_object = Pagination(request,queryset,page_size=10)
    content = {
        "queryset":page_object.page_queryset,
        "page_string":page_object.html()
    }
    print(page_object.html())
    return render(request,"user_list.html",content)

class Myform(BootStrapModelForm):
    class Meta:
        model = models.Userinfo
        fields = ("name","password","age","account","create_time","depart","gender")

def user_add(request):
    if request.method == "GET":
        form = Myform()
        return render(request,"user_add.html",{"form":form})
    form = Myform(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        return render(request,"user_add.html",{"form":form})

def user_edit(request,nid):
    row_object = models.Userinfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = Myform(instance=row_object)
        return render(request,'user_edit.html',{"form":form})
    form = Myform(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request,"user_edit.html",{"form":form})

def user_delete(request,nid):
    Userinfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")