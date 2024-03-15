import logging
from datetime import datetime as dt

import pytz
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from api.handlers.message_handler import MessageHandler
from api.tasks import TaskManager

from .models import Client, Mailing, Message
from .serializers import ClientSerializer, MailingSerializer

logger = logging.getLogger("api")

task_manager = TaskManager()

message_handler = MessageHandler()


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"phone": "Phone number must be unique."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"phone": "Phone number must be unique."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def validate_mailing_editability(self, instance):
        datetime_start = instance.datetime_start
        utc = pytz.UTC
        if utc.localize(dt.now()) > datetime_start:
            raise serializers.ValidationError(
                {"datetime_start": "Cannot edit mailing after it has started"}
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            mailing_id = serializer.data["id"]
            message_handler.create_messages(mailing_id)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except serializers.ValidationError as e:
            logger.error(f"Failed to validate data. Errors: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        self.validate_mailing_editability(instance)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}
            message_handler.update_messages(instance)
            return Response(serializer.data)
        except serializers.ValidationError as e:
            logger.error(f"Failed to validate data. Errors: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.validate_mailing_editability(instance)
        message_handler.delete_messages(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        mailing_id = data["id"]
        messages = Message.objects.filter(mailing=mailing_id).values()
        data["mailing_messages"] = list(messages)
        return Response(data)

    @staff_member_required
    def admin_mailing_detail(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        return render(
            request, "admin/api/mailing/detail.html", {"mailing": mailing}
        )
