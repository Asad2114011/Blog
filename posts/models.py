from django.db import models
from catagories.models import catagory,Tag
from author.models import Author
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=250,unique=True,blank=True)
    content=models.TextField()
    post_image=models.ImageField(upload_to='posts/',blank=True,null=True)
    view_count=models.PositiveIntegerField(default=0)
    catagory=models.ForeignKey(catagory,on_delete=models.PROTECT,related_name='posts')
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='posts')
    tags=models.ManyToManyField(Tag,blank=True,related_name='posts')


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:

        ordering=['-created_at']

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            cur_slug=slugify(self.title)
            slug=cur_slug
            cnt=1
            while Post.objects.filter(slug=slug).exists():
                slug=f"{cur_slug}-{cnt}"
                cnt+=1
            self.slug=slug
        super().save(*args,**kwargs)


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(Author,on_delete=models.CASCADE)
    content=models.TextField(max_length=500)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies')

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.user.name} on {self.post.title}"
    

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    user=models.ForeignKey(Author,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('post','user')
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.user.name} likes {self.post.title}"

class Bookmark(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='bookmarks')
    user=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='bookmarks_user')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('post','user')
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.user.name} bookmarked {self.post.title}"

