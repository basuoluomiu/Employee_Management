from django.shortcuts import render, redirect
from manager.models import Admin
from manager.utils.Pagination import Pagination
from manager.utils.BootStrap import BootStrapModelForm
from django import forms
from manager.utils.encrypt import md5
from django.core.exceptions import ValidationError


def admin_list(request):
    data_dict = {}
    search_data = request.GET.get('query', "")
    if search_data:
        data_dict["username__contains"] = search_data
    queryset = Admin.objects.filter(**data_dict).order_by("id")

    page_object = Pagination(request, queryset)
    content = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    print(queryset)
    return render(request, "admin_list.html", content)


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 钩子函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致！")
        return confirm


def admin_add(request):
    # 新建管理员
    title = "新建管理员"

    if request.method == "GET":
        form = AdminModelForm
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminModelForm(data=request.POST)

    content = {
        "form": form,
        "title": title
    }
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(request, "change.html", content)


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ["username"]


def admin_edit(request, nid):
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, "error.html", {"msg": "无数据"})

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request, nid):
    Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        exists = Admin.objects.filter(id=self.instance.pk, password=md5(pwd))
        if exists:
            raise ValidationError("密码不能一致")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5(confirm) != pwd:
            raise ValidationError("密码不一致")
        return md5(confirm)


def admin_reset(request, nid):
    title = "重置密码"
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, "error.html", {"msg": "无数据"})

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})
