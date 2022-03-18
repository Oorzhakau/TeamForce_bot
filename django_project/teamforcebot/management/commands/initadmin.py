import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        username=os.environ.get('DJANGO_SU_ADMIN')
        email=os.environ.get('DJANGO_SU_EMAIL')
        password=os.environ.get('DJANGO_SU_PASSWORD')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                email=email,
                username=username,
                password=password,
            )