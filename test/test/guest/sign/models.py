# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=100)
    starttime = models.DateTimeField()


    def __unicode__(self):
        return self.name


class Guest(models.Model):
    # 外键
    event = models.ForeignKey(Event)
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

# 设置联合主键
class Meta:
    unique_together = ('event','phone')


def __unicode__(self):
    return self.realname
