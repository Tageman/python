# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from guestapp.models import Novel, Movie, Picture
import requests
from bs4 import BeautifulSoup
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


# 分页（主页/电影/小说/音乐）
def index(request):
    return render(request, 'index.html')


# 电影页面
def movie(request):
    Movie_list = Movie.objects.all()
    return render(request, 'movie.html', {'movies': Movie_list})

page_num = 6
movie_pics = []
movie_names = []
movie_guys = []
movie_directors = []
movie_scores = []
movie_score_imgs = []


# 刷新电影页面
def refresh_movie(request):
    Movie.objects.all().delete()
    for i in range(1, page_num):
        url = 'http://www.imdb.cn/imdb250/' + str(i)
        content = requests.get(url).content
        movie_page_content = BeautifulSoup(content, 'html.parser')
        # 电影封面
        for movie_pic_total in movie_page_content.find_all('div', {'class': 'hong'}):
            for movie_pic in movie_pic_total.find_all('img'):
                movie_pics.append(movie_pic['src'])
        # 电影名称
        for movie_name_total in movie_page_content.find_all('p', {'class': 'bb'}):
            movie_names.append(movie_name_total.text.strip())
        # 电影剧情
        for movie_guy_total in movie_page_content.find_all('div', {'class': 'honghe-5'}):
            movie_guys.append(movie_guy_total.text.strip())
        # 电影导演
        for movie_director_total in movie_page_content.select('p > span'):
            movie_directors.append(movie_director_total.text.strip())
        # 电影评分
        for movie_score_total in movie_page_content.select('span > i'):
            movie_scores.append(movie_score_total.text.strip())
        # 电影评分的图标
        for movie_score_img_total in movie_page_content.select('p > img'):
            movie_score_imgs.append(movie_score_img_total['src'])

    # 插入数据库
    movie_list = []
    movie_num = 150
    for i in range(movie_num):
        movie_list.append(Movie(movie_name=movie_names[i], movie_guy=movie_guys[i], movie_pic=movie_pics[i], movie_director=movie_directors[i], movie_score=movie_scores[i], movie_score_img=movie_score_imgs[i]))
    Movie.objects.bulk_create(movie_list)
    return HttpResponseRedirect('/movie/')





def music(request):
    return render(request, 'music.html')

# 图片页面显示
def picture(request):
    picture_list = Picture.objects.all()
    return render(request, 'picture.html', {'pictures': picture_list})

# 刷新图片页面
pic_img_url = []
def refresh_picture(request):
    Picture.objects.all().delete()
    for i in range(1, 6):
        url = 'https://visualhunt.com/popular/'+str(i)+'/?scolor=Grey'
        content = requests.get(url).content
        picture_page_content = BeautifulSoup(content, 'html.parser')
        for pic_color in picture_page_content.find_all('img', {'class': 'vh-Collage-itemImg'}):
            pic_img_url.append(pic_color['src'])
    pic_list = []
    for i in range(0, len(pic_img_url)):
        pic_list.append(Picture(picture_url=pic_img_url[i]))
    Picture.objects.bulk_create(pic_list)
    return HttpResponseRedirect('/picture/')


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


# 分页
def novel(request):
    Novel_list = Novel.objects.all()
    paginator = Paginator(Novel_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'novel.html', {'novels': contacts})

