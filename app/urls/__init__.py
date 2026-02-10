from .role_permission_urls import urlpatterns as role_permission_urls
from .permission_urls import urlpatterns as permission_urls
from .role_urls import urlpatterns as role_urls
from .user_urls import urlpatterns as user_urls
from .test_url import urlpatterns as test_url
from .booking_urls import urlpatterns as booking_urls
from .venue_urls import urlpatterns as venue_urls
from .event_urls import urlpatterns as event_urls
from .category_urls import urlpatterns as category_urls
from .payment_urls import urlpatterns as payment_urls
from .invoice_urls import urlpatterns as invoice_urls
from .checkin_urls import urlpatterns as checkin_urls
from .event_registration_urls import urlpatterns as event_registration_urls
from .ticket_urls import urlpatterns as ticket_urls
from .user_profile_urls import urlpatterns as user_profile_urls

# Combined urlpatterns so other modules can do `include("app.urls")` and get all app routes.
urlpatterns = (
    role_permission_urls +
    permission_urls +
    role_urls +
    user_urls +
    test_url +
    booking_urls +
    venue_urls +
    event_urls +
    category_urls +
    payment_urls +
    invoice_urls +
    checkin_urls +
    event_registration_urls +
    ticket_urls +
    user_profile_urls
)

__all__ = [
    'urlpatterns',
]
