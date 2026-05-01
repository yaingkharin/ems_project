import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models.booking import Booking
from app.models.ticket import Ticket
from app.models.customer import Customer
from app.models.event import Event
from app.services.booking_service import BookingService

def test_logic():
    # Setup
    customer = Customer.objects.first()
    event = Event.objects.first()
    ticket = Ticket.objects.first()
    
    initial_sold = ticket.sold
    print(f"Initial Sold: {initial_sold}")
    
    # 1. Create Pending Booking
    print("\n--- Creating Pending Booking ---")
    booking = BookingService.create_booking({
        'customer': customer,
        'event': event,
        'ticket': ticket,
        'quantity': 2,
        'total_amount': 20.00,
        'status': 'pending'
    })
    
    ticket.refresh_from_db()
    print(f"Status: {booking.status}, Ticket Sold: {ticket.sold} (Expected: {initial_sold})")
    
    # 2. Confirm Booking
    print("\n--- Confirming Booking ---")
    BookingService.update_booking(booking.id, {'status': 'confirmed'})
    ticket.refresh_from_db()
    print(f"Status: confirmed, Ticket Sold: {ticket.sold} (Expected: {initial_sold + 2})")
    
    # 3. Change Quantity while Confirmed
    print("\n--- Changing Quantity (2 -> 5) while Confirmed ---")
    BookingService.update_booking(booking.id, {'quantity': 5})
    ticket.refresh_from_db()
    print(f"Status: confirmed, Quantity: 5, Ticket Sold: {ticket.sold} (Expected: {initial_sold + 5})")
    
    # 4. Cancel Booking
    print("\n--- Cancelling Booking ---")
    BookingService.update_booking(booking.id, {'status': 'cancelled'})
    ticket.refresh_from_db()
    print(f"Status: cancelled, Ticket Sold: {ticket.sold} (Expected: {initial_sold})")
    
    # Cleanup
    booking.delete()
    print("\nTest completed.")

if __name__ == "__main__":
    test_logic()
