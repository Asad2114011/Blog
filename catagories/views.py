from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .import forms
# Create your views here.
@login_required
def add_tag(request):
    if request.method=='POST':
        tag_form=forms.tagForm(request.POST)
        if tag_form.is_valid():
            tag_form.save()
            return redirect('add_tag')
    else:
        tag_form=forms.tagForm()
    return render(request,'add_tag.html',{'form':tag_form})