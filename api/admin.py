from datetime import datetime as dt

import pytz
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from api.tasks import TaskManager
from api.utils import get_mailing_messages

from .forms import ClientAdminForm, MailingAdminForm
from .models import Client, Mailing

list_per_page = settings.PAGE_SIZE

task_manager = TaskManager()


def mailing_detail(obj):
    url = reverse("api:admin_mailing_detail", args=[obj.id])
    return mark_safe(f"<a href='{url}'>Detail</a>")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    form = MailingAdminForm
    list_display = [
        "id",
        "datetime_start",
        "datetime_end",
        "send_interval_time_start",
        "send_interval_time_end",
        "text",
        "client_filter",
        "clients_count",
        "created_messages",
        "scheduled_messages",
        "delivered_messages",
        "undelivered_messages",
        "cancelled_messages",
        "created_at",
        "updated_at",
        mailing_detail,
    ]
    list_filter = ["datetime_start", "datetime_end", "client_filter"]
    search_fields = ["text", "client_filter"]
    readonly_fields = [
        "clients_count",
        "created_messages",
        "scheduled_messages",
        "delivered_messages",
        "undelivered_messages",
        "cancelled_messages",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "datetime_start"
    list_per_page = list_per_page

    def has_change_permission(self, request, obj=None):
        utc = pytz.UTC
        if obj and utc.localize(dt.now()) > obj.datetime_start:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        obj.save()
        if change:
            messages = get_mailing_messages(obj)
            for message in messages:
                task_manager.update_message_celery_task(message)
        else:
            messages = get_mailing_messages(obj, created=True)
            for message in messages:
                task_manager.create_message_celery_task(message)

    def delete_model(self, request, obj):
        messages = get_mailing_messages(obj)
        for message in messages:
            task_manager.delete_message_celery_task(message)
        obj.delete()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = [
        "id",
        "phone",
        "operator_code",
        "tag",
        "time_zone",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "operator_code",
        "created_at",
        "updated_at",
    ]
    list_filter = ["operator_code", "tag", "time_zone"]
    search_fields = ["phone", "time_zone"]
    list_per_page = list_per_page
