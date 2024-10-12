from random import randint
from django.shortcuts import render
from manager.utils.BootStrap import BootStrapModelForm
from manager.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from manager.utils.Pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        # fields = "__all__"
        exclude = ["oid", "admin"]


def order_list(request):
    queryset = Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset, page_size=5)

    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号生成
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(randint(1000, 9999))
        # 创建用户由session直接获取
        form.instance.admin_id = request.session["info"]["id"]

        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    # 删除订单
    uid = request.GET.get('uid')
    if Order.objects.filter(id=uid).exists():
        Order.objects.filter(id=uid).delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": "删除失败，数据不存在"})


def order_detail(request):
    uid = request.GET.get("uid")
    row_dict = Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)
