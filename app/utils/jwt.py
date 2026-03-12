from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.conf import settings
from app.models.customer import Customer

class JWTUtil:
    """
    Utility class for handling JWT token operations for both Users and Customers.
    """
    @staticmethod
    def generate_tokens(user_or_customer):
        """
        Unified function to generate JWT tokens for both Users and Customers.
        Adds a 'type': 'customer' flag if the object is a Customer.
        """
        refresh = RefreshToken.for_user(user_or_customer)
        
        # Check if it's a Customer instance (it will have 'type' flag set in our previous implementation)
        # but better to check the model name or attributes.
        if user_or_customer.__class__.__name__ == 'Customer':
            refresh['type'] = 'customer'
        
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

    @staticmethod
    def verify_jwt_token(token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            User = get_user_model()
            user = User.objects.get(id=user_id)
            return user
        except TokenError as e:
            raise TokenError(f"Invalid or expired token: {e}")
        except User.DoesNotExist:
            raise TokenError("User not found for the given token.")

    @staticmethod
    def get_user_from_refresh_token(refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh['user_id']
            User = get_user_model()
            user = User.objects.get(id=user_id)
            return user
        except (TokenError, User.DoesNotExist):
            return None

class UniversalJWTAuthentication(JWTAuthentication):
    """
    Universal authenticator that handles both Customers and standard Users.
    Identifies the model to query based on the 'type' claim in the token.
    """
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        if not user_id:
            return None

        # Check if the token belongs to a Customer
        if validated_token.get('type') == 'customer':
            try:
                customer = Customer.objects.get(id=user_id, is_deleted=False)
                return customer
            except Customer.DoesNotExist:
                return None
        
        # Otherwise, treat as a standard User
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
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            if user:
                return (user, validated_token)
            return None
        except (InvalidToken, TokenError):
            return None
