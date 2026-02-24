from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        username=os.getenv('USERNAME')
        email=os.getenv('EMAIL')
        password=os.getenv('PASSWORD')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write('superuser created!')
        else:
            self.stdout.write("superuser already exist!")