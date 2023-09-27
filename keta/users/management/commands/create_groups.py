from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create groups for your custom models'

    def handle(self, *args, **kwargs):
        group_supervisors, created = Group.objects.get_or_create(name="Supervisors")
        group_assistant, created = Group.objects.get_or_create(name='Assistants')
        group_technicians, created = Group.objects.get_or_create(name="Technicians")
        group_operators, created = Group.objects.get_or_create(name='Operators')
        
        self.stdout.write(self.style.SUCCESS('Groups created successfully'))
