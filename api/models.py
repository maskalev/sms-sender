import pytz
from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin
from timezone_field import TimeZoneField

all_timezones = pytz.all_timezones


class Client(ExportModelOperationsMixin("client"), models.Model):
    Timezone = models.TextChoices("Timezone", " ".join(all_timezones))

    phone = models.CharField(max_length=11, unique=True)
    operator_code = models.CharField(max_length=3, db_index=True, blank=True)
    tag = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    time_zone = TimeZoneField(
        use_pytz=True,
        choices=Timezone.choices,
        default=Timezone.UTC,
        choices_display="WITH_GMT_OFFSET",
        db_index=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        self.operator_code = self.phone[1:4]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone

    def get_local_time(self):
        client_time_zone = self.time_zone
        utc_now = timezone.localtime(timezone.now())
        local_time = utc_now.astimezone(client_time_zone).time()
        return local_time


class Mailing(ExportModelOperationsMixin("mailing"), models.Model):
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    text = models.TextField()
    client_filter = models.CharField(max_length=255, blank=True, null=True)
    send_interval_time_start = models.TimeField(blank=True, null=True)
    send_interval_time_end = models.TimeField(blank=True, null=True)
    clients_count = models.IntegerField(default=0)
    created_messages = models.IntegerField(default=0)
    scheduled_messages = models.IntegerField(default=0)
    delivered_messages = models.IntegerField(default=0)
    undelivered_messages = models.IntegerField(default=0)
    cancelled_messages = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def get_mailing_clients(self):
        filter_conditions = models.Q()

        if self.client_filter:
            tags = [tag.strip() for tag in self.client_filter.split(",")]
            for tag in tags:
                filter_conditions |= models.Q(operator_code=tag) | models.Q(
                    tag=tag
                )
        if filter_conditions:
            clients = Client.objects.filter(filter_conditions)
        else:
            clients = Client.objects.all()
        return clients

    def update_messages_info(self):
        self.created_messages = Message.objects.filter(mailing=self.id).count()
        self.scheduled_messages = Message.objects.filter(
            mailing=self.id, status=Message.Status.SCHEDULED
        ).count()
        self.delivered_messages = Message.objects.filter(
            mailing=self.id, status=Message.Status.DELIVERED
        ).count()
        self.undelivered_messages = Message.objects.filter(
            mailing=self.id, status=Message.Status.NOT_DELIVERED
        ).count()
        self.cancelled_messages = Message.objects.filter(
            mailing=self.id, status=Message.Status.CANCELLED
        ).count()
        self.save(
            update_fields=[
                "created_messages",
                "scheduled_messages",
                "delivered_messages",
                "undelivered_messages",
                "cancelled_messages",
            ]
        )

    def set_clients_count(self, clients):
        self.clients_count = len(clients)
        self.save(update_fields=["clients_count"])


class Message(ExportModelOperationsMixin("message"), models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SC", "Scheduled"
        DELIVERED = "DL", "Delivered"
        NOT_DELIVERED = "ND", "Not delivered"
        CANCELLED = "CA", "Cancelled"

    datetime_send = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.SCHEDULED
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.SET_NULL,
        related_name="mailing_messages",
        null=True,
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client_messages"
    )
    celery_task_id = models.CharField(max_length=36, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
