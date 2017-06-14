# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from guestapp.models import Novel
import requests
from bs4 import BeautifulSoup
import threading
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from time import time
from multiprocessing import Process, Pool

# Create your views here.


# 分页（主页/电影/小说/音乐）
def index(request):
    return render(request, 'index.html')


def movie(request):
    return render(request, 'movie.html')


# 分页+跳转页面
def novel(request):
    Novel_list = Novel.objects.all()
    paginator = Paginator(Novel_list,10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'novel.html', {'novels': contacts})


def music(request):
    return render(request, 'music.html')


def picture(request):
    return render(request, 'picture.html')


# 刷新小说
def refresh_novel(request):
    name = []
    num = []
    booklink = []
    bookdetail = []
    Novel.objects.all().delete()
    for i in range(1, 26):
        url = 'http://r.qidian.com/yuepiao?style=1&page=' + str(i)
        content = requests.get(url).content
        rule_content = BeautifulSoup(content, 'html.parser')
        # 爬取书名的函数
        for book in rule_content.find_all('a', {'data-eid': 'qd_C40'}):
            name.append(book.text.strip())

        # 爬取详情的函数
        for bookdetails in rule_content.find_all('p', {'class': 'intro'}):
            bookdetail.append(bookdetails.text.strip())

        # 爬取链接的函数
        for booklinks in rule_content.find_all('a', {'data-eid': 'qd_C40'}):
            linkPattern = re.compile("href=\"(.+?)\"")
            booklink.append(linkPattern.findall(str(booklinks))[0])

        # 爬取月票数的函数
        for book_right_info in rule_content.find_all('div', {'class': 'book-right-info'}):
            for groom in book_right_info.select('p > span'):
                num.append(groom.text.strip())

    # 将数据打包  假设直接在循环中加入数据库操作 每循环一次就会链接一次数据库 所以会造成数据存储数据过慢
    Novel_list = []
    for i in range(500):
        Novel_list.append(Novel(name=name[i], num=num[i], namelink=booklink[i], namedetails=bookdetail[i]))
        # Novel.objects.create(name=name[i], num=num[i], namelink=booklink[i], namedetails=bookdetail[i])
    Novel.objects.bulk_create(Novel_list)
    return HttpResponseRedirect('/novel/')


# 跳转页面
def search_page(request):
    search_page = request.GET.get('novelpage', '')
    return HttpResponseRedirect('/novel/?page={0}'.format(search_page))

# 搜索
def search_novel(request):
    search_novel = request.GET.get('novel', '')
    # 为空就显示全部
    if search_novel == '' or search_novel == 'all' or search_novel.strip() == '':
        return HttpResponseRedirect('/novel/')
    # 号码不为空的时候将匹配filter的号码直接赋值给分页器
    else:
        novel_list_filter = Novel.objects.filter(name__contains=search_novel)
        painator = Paginator(novel_list_filter, 10)
        page = request.GET.get('page')
        try:
            contacts = painator.page(page)
        except PageNotAnInteger:
            contacts = painator.page(1)
        except EmptyPage:
            contacts = painator.page(painator.num_pages)
        return render(request, 'novel.html', {'novels': contacts})



