from django.shortcuts import render,redirect
from .import forms
# Create your views here.
def add_catagory(request):
    if request.method=='POST':
        catagory_form=forms.catagoryForm(request.POST)
        if catagory_form.is_valid():
            catagory_form.save()
            return redirect('add_catagory')
    else:
        catagory_form=forms.catagoryForm()
    return render(request,'add_catagory.html',{'form':catagory_form})