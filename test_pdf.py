import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models.booking import Booking
from app.models.event_ticket import EventTicket
from app.utils.pdf_generator import generate_ticket_pdf

booking = Booking.objects.first()
event_tickets = list(EventTicket.objects.filter(booking=booking))

try:
    buffer = generate_ticket_pdf(booking, event_tickets)
    print("PDF generated successfully, size:", len(buffer.getvalue()))
except Exception as e:
    import traceback
    traceback.print_exc()
