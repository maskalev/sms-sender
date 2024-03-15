from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.handlers.sso_handler import SSOHandler

schema_view = get_schema_view(
    openapi.Info(
        title="SMS sender",
        default_version="v1",
        description="Service for managing SMS mailings",
        contact=openapi.Contact(email="avmaskalev@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


sso_handler = SSOHandler(
    auth0_client_id=settings.AUTH0_CLIENT_ID,
    auth0_client_secret=settings.AUTH0_CLIENT_SECRET,
    auth0_domain=settings.AUTH0_DOMAIN,
)

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/", include("api.urls")),
    path("sso_login", sso_handler.login, name="sso_login"),
    path("sso_logout", sso_handler.logout, name="sso_logout"),
    path("sso_callback", sso_handler.callback, name="sso_callback"),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include("django_prometheus.urls")),
]
