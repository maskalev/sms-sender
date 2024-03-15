from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, MailingViewSet

app_name = "api"

router_v1 = DefaultRouter()

router_v1.register("clients", ClientViewSet)
router_v1.register("mailings", MailingViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path(
        "admin/mailing/<int:mailing_id>/",
        MailingViewSet.admin_mailing_detail,
        name="admin_mailing_detail",
    ),
]
