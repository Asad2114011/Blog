from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    if request.method=='POST':
        print(f"EMAIL USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL PASS: {'SET' if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
        print(f"EMAIL PASS LENGTH: {len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 0}")
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
        try:
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
        except Exception as e:
            print(f"Email failed: {e}")
    
    return redirect('home')
