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

