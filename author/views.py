from django.shortcuts import get_object_or_404, render,redirect
from .import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post
from author.models import Author
# Create your views here.


def register(request):
    if request.method=='POST':
        registerForm=forms.registrationForm(request.POST,request.FILES)
        if registerForm.is_valid():
            user=registerForm.save()
            username=registerForm.cleaned_data.get('username')
            password=registerForm.cleaned_data.get('password1')
            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                messages.success(request,'Account created successfully')
                return redirect('profile')
    else:
        registerForm=forms.registrationForm()
    return render(request,'register.html',{'form':registerForm,'type':'Register'})

def user_login(request):
    if request.method=='POST':
        form=forms.CustomAuthenticationForm(request,request.POST)
        if form.is_valid():
            username_or_email=form.cleaned_data['username']
            user_pass=form.cleaned_data['password']
            user=authenticate(request,username=username_or_email,password=user_pass)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully')
                return redirect('profile')
            else:
                messages.error(request,'Invalid credentials')
    else:
        form=forms.CustomAuthenticationForm()
    return render(request,'login.html',{'form':form,'type':'Login'})

@login_required
def profile(request):
    author=get_object_or_404(Author,user=request.user)
    data=Post.objects.filter(author=author)
    return render(request,'profile.html',{'data':data,'author':author})

@login_required
def edit_profile(request):
    author=get_object_or_404(Author,user=request.user)

    if request.method=='POST':
        profile_form=forms.AuthorUpdateForm(request.POST,request.FILES,instance=author)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form=forms.AuthorUpdateForm(instance=author)
    return render(request,'update_profile.html',{'form':profile_form})

def change_pass(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password updated successfully')
            update_session_auth_hash(request,form.user)
            return redirect('profile')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'pass_change.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('user_login')