from django.db import models


# Create your models here.


# novel
class Novel(models.Model):
    name = models.CharField(max_length=100)
    num = models.IntegerField()
    namelink = models.CharField(max_length=100)
    namedetails = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_name = models.CharField(max_length=1000)
    movie_guy = models.CharField(max_length=1000)
    movie_pic = models.URLField()
    movie_director = models.CharField(max_length=50)
    movie_score = models.FloatField()
    movie_score_img = models.URLField()

    def __str__(self):
        return self.movie_name
