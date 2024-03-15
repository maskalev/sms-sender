import json
from datetime import datetime as dt
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import serializers, status
from rest_framework.test import APIClient

from api.models import Mailing
from api.views import MailingViewSet

api_client = APIClient()


@pytest.mark.django_db
class TestMailingViewSet:
    def test_validate_mailing_editability_past_datetime(
        mailing_view_set, mailing_instance_one
    ):
        past_datetime_start = timezone.now() - timedelta(days=1)
        mailing_instance_one.datetime_start = past_datetime_start
        mailing_instance_one.save()
        with pytest.raises(
            serializers.ValidationError,
            match="Cannot edit mailing after it has started",
        ):
            MailingViewSet().validate_mailing_editability(mailing_instance_one)

    def test_validate_mailing_editability_future_datetime(
        mailing_view_set, mailing_instance_one
    ):
        future_datetime_start = timezone.now() + timedelta(days=1)
        mailing_instance_one.datetime_start = future_datetime_start
        mailing_instance_one.save()
        MailingViewSet().validate_mailing_editability(mailing_instance_one)

    @patch("api.tasks.TaskManager.create_message_celery_task")
    def test_create_mailing(self, mock_create, api_client):
        mailing_data = {
            "datetime_start": timezone.now() - timedelta(days=1),
            "datetime_end": timezone.now() + timedelta(days=1),
            "send_interval_time_start": dt.time(dt(2022, 1, 1, 9, 00)),
            "send_interval_time_end": dt.time(dt(2022, 1, 1, 21, 00)),
            "text": "Test Mailing",
            "client_filter": "Tag",
        }
        response = api_client.post(reverse("api:mailing-list"), mailing_data)
        assert response.status_code == status.HTTP_201_CREATED
        mailing_id = response.data["id"]
        assert Mailing.objects.filter(id=mailing_id).exists()

    @freeze_time("01-01-2024")
    @patch("api.tasks.TaskManager.update_message_celery_task")
    def test_update_mailing(
        self, mock_update, api_client, mailing_instance_one
    ):
        update_data = {
            "text": "New Test Mailing",
        }
        response = api_client.patch(
            reverse("api:mailing-detail", args=[mailing_instance_one.id]),
            update_data,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == update_data["text"]

    @freeze_time("01-01-2024")
    @patch("api.tasks.TaskManager.delete_message_celery_task")
    def test_destroy_mailing(
        self, mock_delete, api_client, mailing_instance_one
    ):
        response = api_client.delete(
            reverse("api:mailing-detail", args=[mailing_instance_one.id])
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_retrieve_mailing(
        self,
        api_client,
        mailing_instance_one,
        message_instance_one,
        message_instance_two,
    ):
        response = api_client.get(
            reverse("api:mailing-detail", args=[mailing_instance_one.id]),
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)["mailing_messages"]) == 2


@pytest.mark.django_db
class TestClientViewSet:
    def test_create_client(self, api_client, client_instance_one):
        client_data = {"phone": "71234567890"}
        response = api_client.post(reverse("api:client-list"), client_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert json.loads(response.content) == {
            "phone": "Phone number must be unique."
        }

    def test_update_client(
        self, api_client, client_instance_one, client_instance_two
    ):
        client_data = {"phone": "71234567890"}
        response = api_client.patch(
            reverse("api:client-detail", args=[client_instance_two.id]),
            client_data,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert json.loads(response.content) == {
            "phone": "Phone number must be unique."
        }
