import os
import django
import sys

# Add project root to path
sys.path.append('D:\\ems_project\\ems_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models.customer import Customer
from app.utils.customer_jwt import generate_customer_tokens
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

def debug_tokens():
    customer = Customer.objects.get(id=1)
    tokens = generate_customer_tokens(customer)
    access_token_str = tokens['access']
    
    print(f"Access Token Claims:")
    token = AccessToken(access_token_str)
    for k, v in token.payload.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    debug_tokens()
