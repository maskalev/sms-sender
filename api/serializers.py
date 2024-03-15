from datetime import datetime as dt

import pytz
from django.core.validators import RegexValidator
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from .models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    time_zone = TimeZoneSerializerField(use_pytz=True, required=False)

    class Meta:
        model = Client
        fields = [
            "id",
            "phone",
            "operator_code",
            "tag",
            "time_zone",
            "created_at",
            "updated_at",
        ]

    phone = serializers.CharField(
        validators=[
            RegexValidator(
                r"^7\d{10}$",
                message="Enter a valid phone number ('7XXXXXXXXXX')",
            )
        ],
        required=True,
        allow_blank=False,
        allow_null=False,
    )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "datetime_send", "mailing", "client", "status"]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = [
            "id",
            "datetime_start",
            "datetime_end",
            "send_interval_time_start",
            "send_interval_time_end",
            "text",
            "client_filter",
            "clients_count",
            "scheduled_messages",
            "created_messages",
            "delivered_messages",
            "undelivered_messages",
            "cancelled_messages",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        datetime_start = (
            data.get("datetime_start") or self.instance.datetime_start
        )
        datetime_end = data.get("datetime_end") or self.instance.datetime_end
        if self.instance:
            send_interval_time_start = (
                data.get("send_interval_time_start")
                or self.instance.send_interval_time_start
            )
            send_interval_time_end = (
                data.get("send_interval_time_end")
                or self.instance.send_interval_time_end
            )
        else:
            send_interval_time_start = data.get("send_interval_time_start")
            send_interval_time_end = data.get("send_interval_time_end")
        utc = pytz.UTC
        if datetime_start > datetime_end:
            raise serializers.ValidationError(
                {
                    "datetime_end": "Datetime end must be later than datetime start"
                }
            )
        if utc.localize(dt.now()) > datetime_end:
            raise serializers.ValidationError(
                {
                    "datetime_end": "Datetime end must be later than the current time"
                }
            )
        if send_interval_time_start and not send_interval_time_end:
            raise serializers.ValidationError(
                {
                    "send_interval_time_end": "'Send interval time end' must be determined"
                }
            )
        if send_interval_time_end and not send_interval_time_start:
            raise serializers.ValidationError(
                {
                    "send_interval_time_start": "'Send interval time start' must be determined"
                }
            )
        return data
