import os
from django.apps import AppConfig


class AppApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Prevent scheduler from starting twice (Django reloader spawns 2 processes)
        if os.environ.get('RUN_MAIN') == 'true':
            from app.scheduler import start_scheduler
            start_scheduler()
