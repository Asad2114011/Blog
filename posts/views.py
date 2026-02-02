from django.shortcuts import render,redirect
from .import forms
# Create your views here.
from .import models
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

@csrf_exempt
def tinymce_upload(request):
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Save to media/tinymce/
        upload_path = os.path.join(settings.MEDIA_ROOT, 'tinymce')
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        file_url = os.path.join(settings.MEDIA_URL, 'tinymce', file.name)
        return JsonResponse({'location': file_url})
    
    return JsonResponse({'error': 'Upload failed'}, status=400)


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
def post_details(request,id):
    post=models.Post.objects.get(id=id)
    return render(request,'post_details.html',{'post':post})

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