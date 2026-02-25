from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings
import resend
import os 



def contact(request):
    if request.method=='POST':
        message=request.POST.get('message','').strip()
        if not message:
            messages.error(request,'Message can not be empty!')
            return redirect('home')
        author=request.user.author_profile

        Contact.objects.create(
            name=author.name,
            email=author.email,
            message=message
        )
        try:
            resend.api_key = os.getenv('RESEND_API_KEY').strip()
            EMAIL=os.getenv('EMAIL')
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": EMAIL,
                "subject": f"New contact message from {author.name}",
                "text": f"Name: {author.name}\nEmail: {author.email}\nMessage: {message}"
            })
            print("Email sent successfully")
        except Exception as e:
            print(f"Email failed: {e}")

        messages.success(request, 'Message sent successfully!')
    
    return redirect('home')
