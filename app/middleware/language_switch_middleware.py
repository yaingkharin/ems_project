from django.utils import translation
from django.conf import settings
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin


class LanguageSwitchMiddleware(MiddlewareMixin):
    """
    Middleware to handle language switching via:
    1. HTTP Header: Accept-Language: km | en
    2. Query Parameter: ?lang=km
    Priority: Query parameter > Header > Default
    """
    
    def process_request(self, request: HttpRequest):
        # Check query parameter first (highest priority)
        lang_param = request.GET.get('lang')
        if lang_param and lang_param in [lang[0] for lang in settings.LANGUAGES]:
            language = lang_param
        else:
            # Check Accept-Language header
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if accept_language:
                # Extract language code from header (e.g., "km", "en-US", "en")
                header_lang = accept_language.split(',')[0].split('-')[0]
                if header_lang in [lang[0] for lang in settings.LANGUAGES]:
                    language = header_lang
                else:
                    language = settings.LANGUAGE_CODE
            else:
                language = settings.LANGUAGE_CODE
        
        # Activate the language
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        # Set language in session for consistency
        if hasattr(request, 'session'):
            request.session['django_language'] = language
