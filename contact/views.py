from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings

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
        messages.success(request,'Message sent successfully!')
        send_mail(
            subject=f"New contact message from {author.name}",
            message=f"""
                Name:{author.name}
                Email:{author.email}
                Message:{message}
                """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    
    return redirect('home')
