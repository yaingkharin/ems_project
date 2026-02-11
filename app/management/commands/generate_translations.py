from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate and compile translation files for all supported languages'

    def handle(self, *args, **options):
        self.stdout.write('Generating translation files...')
        
        # Generate .pot file
        call_command('makemessages', '--locale=en,km', '--verbosity=2')
        
        # Compile translations
        call_command('compilemessages', '--locale=en,km', '--verbosity=2')
        
        self.stdout.write(
            self.style.SUCCESS('Translation files generated and compiled successfully!')
        )
        
        # List available languages
        self.stdout.write('\nAvailable languages:')
        for lang_code, lang_name in settings.LANGUAGES:
            self.stdout.write(f'  - {lang_code}: {lang_name}')
