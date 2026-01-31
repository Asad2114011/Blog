from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from author.models import Author

class registrationForm(UserCreationForm):
    display_name=forms.CharField(max_length=100,label="Display Name")
    email=forms.EmailField(required=True)
    bio=forms.CharField(widget=forms.Textarea,label="Bio")
    profile_image=forms.ImageField(required=False,label="Profile Image")

    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
    field_order = ['username', 'email', 'display_name', 'bio', 'profile_image', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
            Author.objects.create(
                user=user,
                name=self.cleaned_data['display_name'],
                bio=self.cleaned_data['bio'],
                email=self.cleaned_data['email'],
                profile_image=self.cleaned_data.get('profile_image'),
            )
        return user

class changeuserform(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']