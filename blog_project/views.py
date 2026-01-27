from django.shortcuts import render
from posts.models import Post
from catagories.models import catagory

def home(request,catagory_slug=None):
    data=Post.objects.all()
    if catagory_slug is not None:
        catagorys=catagory.objects.get(slug= catagory_slug)
        data=Post.objects.filter(catagory=catagorys)
    catagories=catagory.objects.all()
    return render(request,'home.html',{'data':data,'catagory':catagories})