import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone

logger = logging.getLogger(__name__)


def update_event_statuses():
    """
    Periodic job: syncs the DB status column for every non-cancelled,
    non-deleted event based on the current date/time.
    """
    from app.models.event import Event

    events = Event.objects.filter(is_deleted=False).exclude(status='cancelled')
    updated = 0

    for event in events:
        computed = event.get_computed_status()
        if event.status != computed:
            event.status = computed
            event.save(update_fields=['status', 'updated_at'])
            updated += 1
            logger.info(
                f'[Scheduler] Event #{event.id} "{event.event_name}" '
                f'status changed → {computed}'
            )

    if updated:
        logger.info(f'[Scheduler] {updated} event status(es) updated.')
    else:
        logger.debug('[Scheduler] No event status changes needed.')


def start_scheduler():
    """
    Starts the APScheduler background scheduler.
    Runs update_event_statuses() every 5 minutes.
    """
    scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        update_event_statuses,
        trigger=IntervalTrigger(minutes=5),
        id='update_event_statuses',
        name='Auto-update event statuses every 5 minutes',
        replace_existing=True,
    )

    scheduler.start()
    logger.info('[Scheduler] Event status scheduler started (every 5 min).')
