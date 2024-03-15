from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
import pytz
from django.urls import reverse
from freezegun import freeze_time

from api.admin import mailing_detail
from api.utils import get_mailing_messages

utc = pytz.UTC


@pytest.mark.django_db
def test_mailing_detail(mailing_instance_one):
    obj_link = mailing_detail(mailing_instance_one)
    expected_link = reverse(
        "api:admin_mailing_detail", args=[mailing_instance_one.id]
    )
    assert f"<a href='{expected_link}'>" in obj_link


@freeze_time("2024-01-01 00:00:00")
@pytest.mark.django_db
class TestMailingAdmin:
    def test_has_change_permission(
        self,
        mailing_instance_one,
        mailing_admin,
    ):
        assert (
            mailing_admin.has_change_permission(
                request=None, obj=mailing_instance_one
            )
            is True
        )

        mailing_instance_one.datetime_start = utc.localize(
            datetime.now() - timedelta(days=1)
        )
        mailing_instance_one.save()
        assert (
            mailing_admin.has_change_permission(
                request=None, obj=mailing_instance_one
            )
            is False
        )

    @patch("api.admin.TaskManager.update_message_celery_task")
    @patch("api.admin.TaskManager.create_message_celery_task")
    def test_save_model_new_obj(
        self,
        mock_create_message_celery_task,
        mock_update_message_celery_task,
        mailing_admin,
        mailing_instance_one,
        client_instance_one,
    ):
        mailing_admin.save_model(
            request=None, obj=mailing_instance_one, form=None, change=False
        )
        messages = get_mailing_messages(mailing_instance_one)
        for message in messages:
            mock_create_message_celery_task.assert_called_once_with(message)
        mock_update_message_celery_task.assert_not_called()

    @patch("api.admin.TaskManager.update_message_celery_task")
    @patch("api.admin.TaskManager.create_message_celery_task")
    def test_save_model_change_obj(
        self,
        mock_create_message_celery_task,
        mock_update_message_celery_task,
        mailing_admin,
        mailing_instance_one,
        client_instance_one,
    ):
        mailing_admin.save_model(
            request=None, obj=mailing_instance_one, form=None, change=True
        )
        messages = get_mailing_messages(mailing_instance_one)
        for message in messages:
            mock_update_message_celery_task.assert_called_once_with(message)
        mock_create_message_celery_task.assert_not_called()

    @patch("api.admin.TaskManager.delete_message_celery_task")
    def test_delete_model(
        self,
        mock_delete_message_celery_task,
        mailing_admin,
        mailing_instance_one,
        client_instance_one,
        message_instance_one,
    ):
        messages = get_mailing_messages(mailing_instance_one)
        mailing_admin.delete_model(request=None, obj=mailing_instance_one)
        for message in messages:
            mock_delete_message_celery_task.assert_called_once_with(message)
