import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models.event_ticket import EventTicket

t = EventTicket.objects.first()
if t:
    print(f"Ticket Code: {t.ticket_code}")
    print(f"QR Code exists: {bool(t.qr_code)}")
    if t.qr_code:
        print(f"QR Code Length: {len(t.qr_code)}")
        print(f"QR Code Start: {t.qr_code[:100]}")
else:
    print("No tickets found")
