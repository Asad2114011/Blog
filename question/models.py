from django.db import models
from author.models import Author
from catagories.models import catagory
from django.utils.text import slugify

# Create your models here.
class Question(models.Model):
    title=models.CharField(max_length=300)
    slug=models.SlugField(max_length=200,unique=True,blank=True)
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='user_questions')
    catagory=models.ForeignKey(catagory,on_delete=models.SET_NULL,null=True, blank=True,related_name='questions')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']

    def save(self,*args,**kwargs):
        if not self.slug:
            cur_slug=slugify(self.title)
            slug=cur_slug
            cnt=1
            while Question.objects.filter(slug=slug).exists():
                slug=f"{cur_slug}-{cnt}"
                cnt+=1
            self.slug=slug
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='user_answers')
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']
    
    def __str__(self):
        return f"Answer by {self.author.name}"
    