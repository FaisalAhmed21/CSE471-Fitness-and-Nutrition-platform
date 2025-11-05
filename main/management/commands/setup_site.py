"""
Run this command to configure the Django site for OAuth properly:
python manage.py setup_site
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Setup Site for OAuth configuration'

    def handle(self, *args, **options):
        try:
            site = Site.objects.get(id=1)
            site.domain = '127.0.0.1:8000'
            site.name = 'FitLife Platform'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated site: {site.domain}'))
        except Site.DoesNotExist:
            site = Site.objects.create(id=1, domain='127.0.0.1:8000', name='FitLife Platform')
            self.stdout.write(self.style.SUCCESS(f'Successfully created site: {site.domain}'))
