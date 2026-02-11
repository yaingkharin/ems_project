# Django Internationalization (i18n) Implementation

This document describes the complete internationalization implementation for the Event Management System supporting English and Khmer languages.

## Overview

The i18n implementation provides:
- **Backend-controlled translations**: All messages are translated on the server side
- **Language switching via HTTP headers or query parameters**
- **Professional Khmer translations** used in real Cambodian systems
- **Clean, scalable architecture** following Django best practices

## Architecture

```
ems_project/
├── core/
│   └── settings.py                    # i18n configuration
├── app/
│   ├── middleware/
│   │   └── language_switch_middleware.py  # Language switching logic
│   ├── models/
│   │   └── event.py                   # Model with translated verbose names
│   ├── services/
│   │   └── event_service.py           # Business logic with translations
│   ├── views/
│   │   └── event_views.py             # API responses with translations
│   └── management/commands/
│       └── generate_translations.py   # Translation generation command
└── locale/
    ├── en/
    │   └── LC_MESSAGES/
    │       ├── django.po              # English translations
    │       └── django.mo              # Compiled English translations
    └── km/
        └── LC_MESSAGES/
            ├── django.po              # Khmer translations
            └── django.mo              # Compiled Khmer translations
```

## Configuration

### Django Settings (core/settings.py)

```python
# Supported languages
LANGUAGES = [
    ('en', 'English'),
    ('km', 'Khmer'),
]

# Language code for this installation
LANGUAGE_CODE = 'en'

# Locale paths for translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Enable i18n
USE_I18N = True
USE_L10N = True  # Enable localization for formats
USE_TZ = True

# Middleware order is important!
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # After SessionMiddleware
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]
```

## Language Switching

### Priority Order

1. **Query Parameter** (`?lang=km` or `?lang=en`) - Highest priority
2. **HTTP Header** (`Accept-Language: km` or `Accept-Language: en`)
3. **Default language** (`LANGUAGE_CODE = 'en'`) - Fallback

### API Examples

#### English via Header
```bash
curl -X GET "http://localhost:8000/api/events/" \
  -H "Accept-Language: en" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Khmer via Header
```bash
curl -X GET "http://localhost:8000/api/events/" \
  -H "Accept-Language: km" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### English via Query Parameter
```bash
curl -X GET "http://localhost:8000/api/events/?lang=en" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Khmer via Query Parameter
```bash
curl -X GET "http://localhost:8000/api/events/?lang=km" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Translation Usage

### Models

Use `gettext_lazy` for model verbose names:

```python
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    event_name = models.CharField(max_length=255, verbose_name=_('Event Name'))
    description = models.TextField(verbose_name=_('Description'))
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
```

### Services

Use `gettext` for business logic messages:

```python
from django.utils.translation import gettext as _

class EventService:
    @staticmethod
    def create_event(request_data: dict) -> Event:
        if 'event_name' not in request_data:
            raise ValidationError(_("event_name is required"))
```

### Views

Use `gettext` for API response messages:

```python
from django.utils.translation import gettext as _

def get(self, request):
    events = EventService.get_all_events()
    return api_response(
        data=serializer.data,
        message=_("Events retrieved successfully.")
    )
```

## Available Translations

### English (en)
- All event-related messages
- Booking and ticket messages
- User/authentication messages
- Common API responses
- Pagination messages
- Field names and actions

### Khmer (km)
- Professional Khmer translations
- Used in real Cambodian systems
- Natural phrasing and terminology
- Complete coverage of all English messages

## Translation Files

### Structure
```
locale/
├── en/LC_MESSAGES/
│   ├── django.po    # Source translations
│   └── django.mo    # Compiled translations
└── km/LC_MESSAGES/
    ├── django.po    # Source translations
    └── django.mo    # Compiled translations
```

### Key Translations

#### Event Management
- "Event" → "ព្រឹត្តិការណ៍"
- "Events retrieved successfully." → "ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។"
- "Event created successfully." → "បង្កើតព្រឹត្តិការណ៍ដោយជោគជ័យ។"
- "Event not found." → "រកមិនឃើញព្រឹត្តិការណ៍។"

#### Booking System
- "Booking created successfully." → "បង្កើតការកក់ដោយជោគជ័យ។"
- "Event is fully booked." → "ព្រឹត្តិការណ៍ត្រូវបានកក់ពេញហើយ។"

#### Common Responses
- "Created" → "បានបង្កើត"
- "Updated" → "បានធ្វើបច្ចុប្បន្នភាព"
- "Deleted" → "បានលុប"
- "Not Found" → "រកមិនឃើញ"
- "Permission denied" → "បដិសេធការអនុញ្ញាត"

## Management Commands

### Generate Translations
```bash
python manage.py generate_translations
```

### Manual Commands
```bash
# Generate .pot files
python manage.py makemessages --locale=en,km

# Compile translations
python manage.py compilemessages --locale=en,km
```

## Frontend Integration

### JavaScript/axios
```javascript
// English
const response = await axios.get('/api/events/', {
  headers: { 'Accept-Language': 'en' }
});

// Khmer
const response = await axios.get('/api/events/', {
  headers: { 'Accept-Language': 'km' }
});
```

### React Component
```javascript
const [language, setLanguage] = useState('en');

const fetchEvents = async () => {
  const response = await axios.get(`/api/events/?lang=${language}`);
  setMessage(response.data.message); // Translated message
};
```

## Best Practices

### Backend Rules
1. **No hardcoded strings** in views or services
2. **Use `gettext_lazy`** for model definitions
3. **Use `gettext`** for runtime messages
4. **Backend is single source of truth** for all translations
5. **Consistent translation keys** across all modules

### Frontend Rules
1. **No translation logic** in frontend code
2. **Switch language via header or query parameter**
3. **Display translated messages** from API responses
4. **Handle language switching** at the HTTP request level

### Development Workflow
1. **Add translatable strings** using `_()` or `gettext()`
2. **Run `makemessages`** to update .pot files
3. **Translate new strings** in .po files
4. **Run `compilemessages`** to generate .mo files
5. **Test both languages** in API responses

## Response Examples

### English Response
```json
{
  "success": true,
  "message": "Events retrieved successfully.",
  "data": [...]
}
```

### Khmer Response
```json
{
  "success": true,
  "message": "ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។",
  "data": [...]
}
```

## Testing

### Unit Tests
```python
from django.test import TestCase
from django.utils.translation import activate

class EventI18nTest(TestCase):
    def test_english_messages(self):
        activate('en')
        response = self.client.get('/api/events/')
        self.assertEqual(response.data['message'], 'Events retrieved successfully.')
    
    def test_khmer_messages(self):
        activate('km')
        response = self.client.get('/api/events/')
        self.assertEqual(response.data['message'], 'ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។')
```

### API Testing
```bash
# Test English
curl -H "Accept-Language: en" http://localhost:8000/api/events/

# Test Khmer  
curl -H "Accept-Language: km" http://localhost:8000/api/events/

# Test query parameter
curl "http://localhost:8000/api/events/?lang=km"
```

## Deployment Considerations

### Production Settings
```python
# Ensure USE_I18N = True in production
# Compile translations before deployment
# Test both languages in staging environment
```

### Performance
- Translations are compiled to .mo files for fast loading
- Language detection is efficient middleware
- No runtime translation compilation

## Maintenance

### Adding New Languages
1. Add language to `LANGUAGES` setting
2. Create locale directory: `locale/xx/LC_MESSAGES/`
3. Run `makemessages --locale=xx`
4. Translate all strings in .po file
5. Run `compilemessages --locale=xx`

### Updating Translations
1. Add new translatable strings to code
2. Run `makemessages` to update .pot files
3. Update .po files with new translations
4. Run `compilemessages` to regenerate .mo files

## Troubleshooting

### Common Issues
1. **Translations not working**: Check middleware order
2. **Missing translations**: Run `compilemessages`
3. **Wrong language**: Check Accept-Language header format
4. **Khmer encoding issues**: Ensure UTF-8 in .po files

### Debug Commands
```bash
# Check available languages
python manage.py shell
>>> from django.conf import settings
>>> settings.LANGUAGES

# Test translation
python manage.py shell
>>> from django.utils.translation import gettext as _
>>> _('Event not found.')
```

This implementation provides a complete, production-ready internationalization system for the Event Management System with professional English and Khmer support.
