from django.test import TestCase
from django.utils.translation import activate, gettext as _
from django.test.client import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()


class I18nTestCase(TestCase):
    """
    Test cases for internationalization functionality
    """
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.auth_header = f'Bearer {refresh.access_token}'
    
    def test_english_language_via_header(self):
        """Test English language via Accept-Language header"""
        activate('en')
        
        response = self.client.get(
            '/api/events/',
            HTTP_ACCEPT_LANGUAGE='en',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Events retrieved successfully.')
    
    def test_khmer_language_via_header(self):
        """Test Khmer language via Accept-Language header"""
        activate('km')
        
        response = self.client.get(
            '/api/events/',
            HTTP_ACCEPT_LANGUAGE='km',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។')
    
    def test_english_language_via_query_param(self):
        """Test English language via query parameter"""
        response = self.client.get(
            '/api/events/?lang=en',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Events retrieved successfully.')
    
    def test_khmer_language_via_query_param(self):
        """Test Khmer language via query parameter"""
        response = self.client.get(
            '/api/events/?lang=km',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។')
    
    def test_language_priority_query_over_header(self):
        """Test that query parameter has priority over header"""
        response = self.client.get(
            '/api/events/?lang=km',
            HTTP_ACCEPT_LANGUAGE='en',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        # Query parameter should win
        self.assertEqual(response_data['message'], 'ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។')
    
    def test_default_language_fallback(self):
        """Test fallback to default language when unsupported language is provided"""
        response = self.client.get(
            '/api/events/',
            HTTP_ACCEPT_LANGUAGE='fr',  # Unsupported language
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        # Should fallback to English (default)
        self.assertEqual(response_data['message'], 'Events retrieved successfully.')
    
    def test_model_translations(self):
        """Test model field translations"""
        from app.models.event import Event
        
        # Test English
        activate('en')
        event_en = Event()
        self.assertEqual(str(event_en._meta.verbose_name), 'Event')
        self.assertEqual(str(event_en._meta.verbose_name_plural), 'Events')
        
        # Test Khmer
        activate('km')
        event_km = Event()
        self.assertEqual(str(event_km._meta.verbose_name), 'ព្រឹត្តិការណ៍')
        self.assertEqual(str(event_km._meta.verbose_name_plural), 'ព្រឹត្តិការណ៍')
    
    def test_service_translations(self):
        """Test service layer translations"""
        from app.services.event_service import EventService
        from django.core.exceptions import ValidationError
        
        # Test English
        activate('en')
        try:
            EventService.create_event({})  # Empty data should trigger validation
        except ValidationError as e:
            self.assertIn('event_name is required', str(e))
        
        # Test Khmer
        activate('km')
        try:
            EventService.create_event({})  # Empty data should trigger validation
        except ValidationError as e:
            self.assertIn('event_name តម្រូវបានទាមទារ', str(e))
    
    def test_gettext_function(self):
        """Test direct gettext function"""
        # Test English
        activate('en')
        self.assertEqual(_('Event not found.'), 'Event not found.')
        
        # Test Khmer
        activate('km')
        self.assertEqual(_('Event not found.'), 'រកមិនឃើញព្រឹត្តិការណ៍។')
    
    def test_language_persistence_in_session(self):
        """Test that language is stored in session"""
        # Set language via query parameter
        self.client.get(
            '/api/events/?lang=km',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        # Check if language is stored in session
        session = self.client.session
        self.assertEqual(session.get('django_language'), 'km')
