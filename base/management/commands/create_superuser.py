from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **kwargs):
        DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
        DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')
        DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        if DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD:
            if not User.objects.filter(username=DJANGO_SUPERUSER_USERNAME).exists():
                User.objects.create_superuser(DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD)
                self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
            else:
                self.stdout.write('Superuser already exists.')
