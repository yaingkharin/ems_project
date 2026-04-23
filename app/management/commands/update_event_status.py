from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models.event import Event


class Command(BaseCommand):
    help = 'Auto-update event status in the DB based on current date/time. Skips cancelled events.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Updating event statuses...'))

        events = Event.objects.filter(is_deleted=False).exclude(status='cancelled')
        updated = 0

        for event in events:
            computed = event.get_computed_status()
            if event.status != computed:
                event.status = computed
                event.save(update_fields=['status'])
                updated += 1
                self.stdout.write(
                    f'  [Updated] Event #{event.id} "{event.event_name}" '
                    f'{event.status!r} -> {computed!r}'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. {updated} event(s) updated out of {events.count()} checked.'
            )
        )
