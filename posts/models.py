from django.db import models
from catagories.models import catagory
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=40)
    content=models.TextField()
    catagory=models.ManyToManyField(catagory)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title