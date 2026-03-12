from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from app.models.customer import Customer
from django.contrib.auth import get_user_model
from django.conf import settings

def generate_customer_tokens(customer):
    """
    Generates access and refresh tokens for a Customer using standard user_id claim
    and a custom 'type': 'customer' flag to distinguish from regular Users.
    """
    refresh = RefreshToken.for_user(customer)
    refresh['type'] = 'customer'
    
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }

class CustomerJWTAuthentication(JWTAuthentication):
    """
    Universal authentication class that handles both Customers and standard Users.
    """
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        if not user_id:
            return None

        # Check if this is a customer token based on our custom flag
        if validated_token.get('type') == 'customer':
            try:
                customer = Customer.objects.get(id=user_id, is_deleted=False)
                return customer
            except Customer.DoesNotExist:
                return None
        
        # Otherwise, handle as a standard User
        try:
            User = get_user_model()
            return User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            return None

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            # Try to validate the token
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            
            if user:
                return (user, validated_token)
            return None
        except (InvalidToken, TokenError):
            return None
