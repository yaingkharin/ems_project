from django.core.management.base import BaseCommand
from app.seeds.permission_seed import seed_permissions
from app.seeds.role_seed import seed_roles
from app.seeds.user_seed import seed_users

class Command(BaseCommand):
    help = 'Seeds initial data for permissions, roles, and users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Starting data seeding...'))

        self.stdout.write(self.style.HTTP_INFO('Seeding Permissions...'))
        seed_permissions()
        self.stdout.write(self.style.SUCCESS('Permissions seeded successfully.'))

        self.stdout.write(self.style.HTTP_INFO('Seeding Roles...'))
        seed_roles()
        self.stdout.write(self.style.SUCCESS('Roles seeded successfully.'))

        self.stdout.write(self.style.HTTP_INFO('Seeding Users...'))
        seed_users()
        self.stdout.write(self.style.SUCCESS('Users seeded successfully.'))

        self.stdout.write(self.style.SUCCESS('Data seeding completed.'))
