from django.shortcuts import render,redirect,HttpResponse
from django import forms
from io import BytesIO
from manager import models
from manager.utils.BootStrap import BootStrapForm
from manager.utils.encrypt import md5

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

def account_login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password","用户名或密码错误")
            return render(request, "login.html", {"form": form})
        request.session["info"] = {'id':admin_object.id,'name':admin_object.username}
        return redirect("/index")
    return render(request, "login.html", {"form": form})

def account_logout(request):
    request.session.clear()
    return redirect('/login/')
