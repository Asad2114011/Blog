from django.db import models
from django.utils.text import slugify

# Create your models here.
class catagory(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)

    class Meta:
        ordering=['name']
    
class Tag(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=60,unique=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            cur_slug=slugify(self.name)
            slug=cur_slug
            cnt=1
            while catagory.objects.filter(slug=slug).exists():
                slug=f"{cur_slug}-{cnt}"
                cnt+=1
            self.slug=slug
        super().save(*args,**kwargs)

    class Meta:
        ordering=['name']
    