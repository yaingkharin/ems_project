from django.core.management.base import BaseCommand
from app.seeds.report_test_seed import seed_report_data

class Command(BaseCommand):
    help = 'Seeds mockup data for testing the reporting functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Starting report data seeding...'))

        try:
            seed_report_data()
            self.stdout.write(self.style.SUCCESS('Report data seeded successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding data: {e}'))

        self.stdout.write(self.style.SUCCESS('Data seeding process finished.'))
