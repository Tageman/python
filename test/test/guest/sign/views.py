# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  django.http import HttpResponse, HttpResponseRedirect
from  django.contrib import auth
from  django.contrib.auth.decorators import login_required
from  sign.models import Event, Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # if username == 'admin' and password == '123456':
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # 将地址重定向（作用仅仅是在显示地址的地方显示 显示之后在URL查找event_manage.html）
            response = HttpResponseRedirect('/event_manage/')
            # 添加浏览器cookie
            # response.set_cookie('user', username, 3600)
            # 设置session
            request.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': '用户名or密码错误！'})


# 防止用户直接访问页面
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')
    event_list = Event.objects.all()

    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username,'events':event_list})

@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html', {'user': username,'events':event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    # 先将数据库中的数据取出来放在guest_list中
    guest_list = Guest.objects.all()
    painator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = painator.page(page)
    except PageNotAnInteger:
        contacts = painator.page(1)
    except EmptyPage:
        contacts = painator.page(painator.num_pages)
    return render(request, 'guest_manage.html', {'user': username, 'guests': contacts})

@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get('phone', '')
    # 为空就显示全部
    if search_phone == '':
        username = request.session.get('user', '')
        # 先将数据库中的数据取出来放在guest_list中
        guest_list_all = Guest.objects.all()
        painator = Paginator(guest_list_all, 2)
        page = request.GET.get('page')
        try:
            contacts = painator.page(page)
        except PageNotAnInteger:
            contacts = painator.page(1)
        except EmptyPage:
            contacts = painator.page(painator.num_pages)
        return render(request, 'guest_manage.html', {'user': username, 'guests': contacts})
    # 号码不为空的时候将匹配filter的号码直接赋值给分页器
    else:
        guest_list_filter = Guest.objects.filter(phone__contains=search_phone)
        painator = Paginator(guest_list_filter, 2)
        page = request.GET.get('page')
        try:
            contacts = painator.page(page)
        except PageNotAnInteger:
            contacts = painator.page(1)
        except EmptyPage:
            contacts = painator.page(painator.num_pages)
        return render(request, 'guest_manage.html', {'user': username, 'guests': contacts})
