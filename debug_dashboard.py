import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from app.models.booking import Booking
from django.db.models import Sum
from django.utils import timezone
import datetime

today = timezone.now()
day_date = today.date()
print(f"Today (UTC): {today}")
print(f"Target Date: {day_date}")

qs = Booking.objects.filter(status='confirmed', created_at__date=day_date)
print(f"Count: {qs.count()}")
print(f"Sum: {qs.aggregate(total=Sum('total_amount'))['total']}")

# List all bookings today
for b in Booking.objects.filter(created_at__date=day_date):
    print(f"ID: {b.id}, Status: {b.status}, Amount: {b.total_amount}, CreatedAt: {b.created_at}")

# Try without __date
start_of_day = timezone.make_aware(datetime.datetime.combine(day_date, datetime.time.min))
end_of_day = timezone.make_aware(datetime.datetime.combine(day_date, datetime.time.max))
qs2 = Booking.objects.filter(status='confirmed', created_at__range=(start_of_day, end_of_day))
print(f"Range Count: {qs2.count()}")
