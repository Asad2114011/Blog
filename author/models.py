from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Author(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="author_profile")
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=120,unique=True,blank=True)
    bio=models.TextField()
    email=models.EmailField(max_length=100)
    profile_image=models.ImageField(upload_to='authors/',blank=True,null=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.user.username)
        super().save(*args,**kwargs)