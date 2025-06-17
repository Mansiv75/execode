# submissions/management/commands/seed_languages.py
from django.core.management.base import BaseCommand
from languages.models import Language

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        languages = [
            {"name": "Python 3", "slug": "python", "version": "3.10"},
            {"name": "C++", "slug": "cpp", "version": "17"},
            {"name": "Java", "slug": "java", "version": "17"},
        ]
        for lang in languages:
            Language.objects.get_or_create(**lang)
        self.stdout.write(self.style.SUCCESS("Languages seeded"))
