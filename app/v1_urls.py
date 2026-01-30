from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from app.views.auth_views import RegisterView, LoginView, LogoutView

schema_view = get_schema_view(
    openapi.Info(
        title="Event Management System API",
        default_version='v1',
        description="API documentation for the Event Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@events.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('v1/', include([
        path('auth/', include([
            path('register/', RegisterView.as_view(), name='register'),
            path('login/', LoginView.as_view(), name='login'),
            path('logout/', LogoutView.as_view(), name='logout'),
        ])),
        path('roles/', include('app.urls.role_urls')),
        path('users/', include('app.urls.user_urls')),
        path('permissions/', include('app.urls.permission_urls')),
        path('role_permissions/', include('app.urls.role_permission_urls')),
        path('venue/', include('app.urls.venue_urls')),
    ])),

    # Swagger UI and ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]