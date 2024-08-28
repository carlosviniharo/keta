# myapp/management/commands/update_field.py
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from tasks.models import Jtareasticket, Jestados


class Command(BaseCommand):
    help = 'Update the state of the tickets based on the date allowed'

    def handle(self, *args, **kwargs):
        today = timezone.now()

        # Get the state expired
        expired_state = Jestados.objects.get(pk=9)

        # Bulk update the state for expired tasks
        expired_tasks = Jtareasticket.objects.annotate(
            fecha_final=Coalesce('fechaextension', 'fechaentrega')
            ).filter(
            fecha_final__lt=today
            ).exclude(
            idestado__in=[6, 7, 8, 9]
        )

        # Extract the IDs of the tasks that will be updated
        task_ids = list(expired_tasks.values_list('idtarea', flat=True))

        # Bulk update the state for expired tasks
        expired_tasks.update(idestado=expired_state)

        # Print the IDs of the updated tasks
        self.stdout.write(
            f"Successfully updated the following tasks: {', '.join(map(str, task_ids))}")
