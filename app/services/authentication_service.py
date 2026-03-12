from typing import Optional
from app.models.customer import Customer
from app.models.role import Role
from app.services.google_oauth_service import GoogleOAuthService
from app.utils.jwt import JWTUtil
from rest_framework.exceptions import AuthenticationFailed

class AuthenticationService:
    @staticmethod
    def google_login(token: str) -> dict:
        """
        Handles Google OAuth login/registration for Customers.
        """
        # 1. Verify Google Token
        google_user_data = GoogleOAuthService.verify_google_token(token)
        
        if not google_user_data.get('email_verified'):
            raise AuthenticationFailed('Google account email is not verified.')

        email = google_user_data['email']
        
        # 2. Check if customer exists, else create
        # Fetch the default 'User' role
        try:
            default_role = Role.objects.get(name='User')
        except Role.DoesNotExist:
            default_role = None

        customer, created = Customer.objects.update_or_create(
            email=email,
            defaults={
                'first_name': google_user_data.get('first_name', ''),
                'last_name': google_user_data.get('last_name', ''),
                'picture': google_user_data.get('picture', ''),
                'email_verified': True,
                'is_deleted': False,
                'role': default_role
            }
        )

        # 4. Generate JWT tokens (Unified)
        tokens = JWTUtil.generate_tokens(customer)
        
        return {
            'tokens': tokens,
            'customer': {
                'id': customer.id,
                'email': customer.email,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'picture': customer.picture,
                'role': customer.role.name if customer.role else None
            },
        }
