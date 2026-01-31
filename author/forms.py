from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from author.models import Author

class registrationForm(UserCreationForm):
    display_name=forms.CharField(max_length=100,label="Display Name",widget=forms.TextInput(attrs={'placeholder':'Enter your display name'}))
    email=forms.EmailField(required=True,label="Email",widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    bio=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write your bio here..'}),label="Bio")
    profile_image=forms.ImageField(required=False,label="Profile Image")
  

    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password'
        })
        
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

class CustomAuthenticationForm(AuthenticationForm):
    username=forms.CharField(
        label='Username or Email',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder':'Enter username or email'})
    )
    password=forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder':'Enter password'})
    )

class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model=Author
        fields=['name','email','bio','profile_image']
        labels = {
            'name':'Display Name'
        }
        widgets={
            'bio':forms.Textarea(attrs={'row':4})
        }
        
    def save(self, commit=True):
        author = super().save(commit=False)
        
        if commit:
            author.save()
            author.user.email = author.email
            author.user.save()
        
        return author
   