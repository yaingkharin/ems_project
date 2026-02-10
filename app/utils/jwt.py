from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken

def generate_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def verify_jwt_token(token):
    try:
        
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        User = get_user_model() # Get User model here
        user = User.objects.get(id=user_id)
        return user
    except TokenError as e:
        raise TokenError(f"Invalid or expired token: {e}")
    except User.DoesNotExist:
        raise TokenError("User not found for the given token.")

def get_user_from_refresh_token(refresh_token):
    try:
        refresh= RefreshToken(refresh_token)
        user_id = refresh['user_id']
        User = get_user_model() # Get User model here
        user = User.objects.get(id=user_id)
        return user
    except (TokenError, User.DoesNotExist):
        return None