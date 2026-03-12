from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class GoogleOAuthService:
    @staticmethod
    def verify_google_token(token: str) -> dict:
        """
        Verifies the Google ID token and returns user information.
        """
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            # We allow both your ID and the Google Playground ID for easier testing
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                audience=[
                    settings.GOOGLE_CLIENT_ID,
                    '407408718192.apps.googleusercontent.com' # Google Playground default
                ]
            )

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            # userid = idinfo['sub']
            
            # Verify issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise AuthenticationFailed('Wrong issuer.')

            return {
                'email': idinfo.get('email'),
                'first_name': idinfo.get('given_name', ''),
                'last_name': idinfo.get('family_name', ''),
                'picture': idinfo.get('picture', ''),
                'email_verified': idinfo.get('email_verified', False)
            }
        except ValueError as e:
            # Invalid token
            raise AuthenticationFailed(f'Invalid Google token: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Google verification failed: {str(e)}')
