from django.db import models


class Department(models.Model):
    """部门表"""
    title = models.CharField(max_length=32, verbose_name='部门名称')

    def __str__(self):
        return self.title


class Userinfo(models.Model):
    """员工表"""
    name = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='余额', default=0)
    create_time = models.DateField(verbose_name='入职时间')

    depart = models.ForeignKey(verbose_name='部门', to=Department, to_field="id", on_delete=models.CASCADE)
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name='性别')


class Admin(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")

    def __str__(self):
        return self.username


class Task(models.Model):
    # 任务表
    level_choice = [
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")
    ]
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=3)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详情")
    user = models.ForeignKey(verbose_name="负责人", to=Admin, on_delete=models.CASCADE)


class Order(models.Model):
# 订单表
    oid = models.CharField(verbose_name='订单号',max_length=64)
    title = models.CharField(verbose_name='名称',max_length=32)
    price = models.IntegerField(verbose_name='价格',)

    status_choices = [
        (1,"待支付"),
        (2,"已支付")
    ]
    status = models.SmallIntegerField(verbose_name='状态',choices=status_choices,default=1)
    admin = models.ForeignKey(verbose_name='管理员',to='Admin',on_delete=models.CASCADE)