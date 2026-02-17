from django import forms
from .models import Tag

class tagForm(forms.ModelForm):
    class Meta:
        model=Tag
        fields=['name']