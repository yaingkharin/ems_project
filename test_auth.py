import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models.customer import Customer
from app.utils.jwt import JWTUtil
from django.test import Client

c = Customer.objects.first()
if c:
    print(f"Testing with customer: {c.email}")
    tokens = JWTUtil.generate_tokens(c)
    access = tokens['access_token']
    client = Client()
    # Try an existing booking first if possible, or just 52
    from app.models.booking import Booking
    b = Booking.objects.first()
    b_id = b.id if b else 52
    
    print(f"Requesting /api/v1/bookings/{b_id}/ticket/")
    res = client.get(f'/api/v1/bookings/{b_id}/ticket/', HTTP_AUTHORIZATION=f'Bearer {access}')
    print(f"Status: {res.status_code}")
    if res.status_code != 200:
        with open('error.html', 'wb') as f:
            f.write(res.content)
        print("Error saved to error.html")
else:
    print("No customer found")
