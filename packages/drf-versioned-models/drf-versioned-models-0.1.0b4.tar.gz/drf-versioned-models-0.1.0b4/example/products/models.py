import uuid

from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='商品ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='商品名称')


class Price(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')


class ProductProfile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    title = models.CharField(max_length=128, verbose_name='商品名称')
    description = models.CharField(max_length=128, verbose_name='商品描述')
