from django.shortcuts import render,redirect
from .import forms
# Create your views here.
from .import models
from django.contrib.auth.decorators import login_required


@login_required
def create_post(request):
    if request.method=='POST':
        post_form=forms.PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            post=post_form.save(commit=False)
            post.author=request.user.author_profile
            post.save()
            post_form.save_m2m()
            return redirect('profile')
    else:
        post_form=forms.PostForm()
    return render(request,'create_post.html',{'form':post_form})

@login_required
def edit_post(request,id):
    post =models.Post.objects.get(pk=id)
    post_form=forms.PostForm(instance=post)

    if request.method=='POST':
        post_form=forms.PostForm(request.POST,request.FILES,instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('home')
   
    return render(request,'edit_post.html',{'form':post_form})

@login_required
def delete_post(request,id):
     post =models.Post.objects.get(pk=id)
     post.delete()
     return redirect('home')