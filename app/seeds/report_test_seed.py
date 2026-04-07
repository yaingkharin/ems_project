import random
from datetime import timedelta
from django.utils import timezone
from app.models.category import Category
from app.models.venue import Venue
from app.models.event import Event
from app.models.ticket import Ticket
from app.models.customer import Customer
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.checkin import Checkin

def seed_report_data():
    """
    Seeds mockup data to test reporting functionality.
    """
    print("Seeding testing data for reports...")

    # 1. Categories
    cat_music, _ = Category.objects.get_or_create(category_name="Music", defaults={'description': "Musical events"})
    cat_tech, _ = Category.objects.get_or_create(category_name="Technology", defaults={'description': "Tech workshops"})

    # 2. Venues
    venue_hall, _ = Venue.objects.get_or_create(
        name="Grand Hall", 
        defaults={'address': "123 Main St", 'capacity': 500}
    )
    venue_stadium, _ = Venue.objects.get_or_create(
        name="City Stadium", 
        defaults={'address': "456 Stadium Way", 'capacity': 5000}
    )

    # 3. Events
    # One in the past (Completed)
    event_past, _ = Event.objects.get_or_create(
        event_name="Summer Rock Fest 2025",
        defaults={
            'description': "Annual rock festival",
            'location': "City Stadium",
            'event_date': timezone.now().date() - timedelta(days=30),
            'start_time': "18:00:00",
            'end_time': "23:00:00",
            'organizer': "Rock Agency",
            'category': cat_music,
            'venue': venue_stadium,
            'status': 'completed'
        }
    )

    # One in the future (Upcoming)
    event_future, _ = Event.objects.get_or_create(
        event_name="AI Summit 2026",
        defaults={
            'description': "The future of AI",
            'location': "Grand Hall",
            'event_date': timezone.now().date() + timedelta(days=90),
            'start_time': "09:00:00",
            'end_time': "17:00:00",
            'organizer': "Tech Corp",
            'category': cat_tech,
            'venue': venue_hall,
            'status': 'upcoming'
        }
    )

    # 4. Tickets
    t_rock_vip, _ = Ticket.objects.get_or_create(event=event_past, ticket_type="VIP", defaults={'price': 150.00, 'quantity': 50, 'sold': 0})
    t_rock_gen, _ = Ticket.objects.get_or_create(event=event_past, ticket_type="General", defaults={'price': 50.00, 'quantity': 450, 'sold': 0})

    t_ai_early, _ = Ticket.objects.get_or_create(event=event_future, ticket_type="Early Bird", defaults={'price': 200.00, 'quantity': 100, 'sold': 0})
    t_ai_std, _ = Ticket.objects.get_or_create(event=event_future, ticket_type="Standard", defaults={'price': 350.00, 'quantity': 400, 'sold': 0})

    # 5. Customers
    customers = []
    for i in range(10):
        c, _ = Customer.objects.get_or_create(
            email=f"tester{i}@example.com",
            defaults={'first_name': f"Test{i}", 'last_name': f"User{i}"}
        )
        customers.append(c)

    # 6. Bookings & Payments
    # Let's create a mix for Summer Rock Fest
    for i in range(5):
        cust = customers[i]
        qty = random.randint(1, 3)
        t_type = t_rock_vip if i % 2 == 0 else t_rock_gen
        total = float(t_type.price) * qty
        
        booking = Booking.objects.create(
            customer=cust,
            event=event_past,
            ticket=t_type,
            quantity=qty,
            total_amount=total,
            status='confirmed',
            booking_date=timezone.now() - timedelta(days=35)
        )
        t_type.sold += qty
        t_type.save()

        # Completed payment
        Payment.objects.create(
            booking=booking,
            amount=total,
            payment_method='bakong',
            status='completed',
            paid=True,
            paid_at=timezone.now() - timedelta(days=35)
        )

        # Some check-ins for attendance
        if i < 4: # 4 out of 5 check in
            Checkin.objects.create(
                booking=booking,
                status='checked_in',
                checkin_time=booking.booking_date + timedelta(days=5),
                ticket_code=f"ROCK-VIP-{booking.id}" if t_type == t_rock_vip else f"ROCK-GEN-{booking.id}"
            )

    # Let's create some for AI Summit
    for i in range(5, 10):
        cust = customers[i]
        qty = 1
        t_type = t_ai_early
        total = float(t_type.price) * qty
        
        status = 'confirmed' if i < 8 else 'pending'
        
        booking = Booking.objects.create(
            customer=cust,
            event=event_future,
            ticket=t_type,
            quantity=qty,
            total_amount=total,
            status=status,
            booking_date=timezone.now() - timedelta(days=2)
        )
        t_type.sold += qty
        t_type.save()

        if status == 'confirmed':
            # Completed cash
            Payment.objects.create(
                booking=booking,
                amount=total,
                payment_method='cash',
                status='completed',
                paid=True,
                paid_at=timezone.now() - timedelta(days=2)
            )
        else:
            # Pending payment
            Payment.objects.create(
                booking=booking,
                amount=total,
                payment_method='bakong',
                status='pending',
                paid=False
            )

    print("Seeding completed successfully.")
