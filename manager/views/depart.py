from django.shortcuts import render,redirect
from manager import models
from manager.models import Department

def depart_list(request):
    # 部门列表
    departments = models.Department.objects.all()
    return render(request,"depart_list.html",{"departments":departments})

def depart_add(request):
    # 添加部门
    if request.method == "GET":
        return render(request,"depart_add.html")
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list")

def depart_delete(request):
    # 删除部门
    nid = request.GET.get("nid")
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

def depart_edit(request,nid):
    # 编辑部门
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,"depart_edit.html",{"row_object":row_object})
    title = request.POST.get("title")
    Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
