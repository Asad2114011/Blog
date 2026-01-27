from django import forms
from .models import catagory

class catagoryForm(forms.ModelForm):
    class Meta:
        model=catagory
        fields='__all__'