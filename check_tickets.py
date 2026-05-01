import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from app.models.ticket import Ticket
from django.db.models import Sum

res = Ticket.objects.aggregate(total=Sum('quantity'))
print(f"Total Quantity: {res['total']}")

# List all tickets
for t in Ticket.objects.all():
    print(f"ID: {t.id}, Type: {t.ticket_type}, Qty: {t.quantity}, Sold: {t.sold}, Event: {t.event.event_name}")
