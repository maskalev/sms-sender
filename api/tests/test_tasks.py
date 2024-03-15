from datetime import datetime as dt
from unittest.mock import patch

import pytest
import pytz
from freezegun import freeze_time

from api.models import Message
from api.tasks import (
    TaskManager,
    get_mailings_stats,
    send_daily_statistics_email,
    send_mailing,
)

utc = pytz.UTC


@pytest.mark.django_db
@patch("api.tasks.send_mail")
def test_send_daily_statistics_email(mock_send_mail):
    send_daily_statistics_email()
    mock_send_mail.assert_called_once()


@pytest.mark.django_db
class TestSendMailing:
    @patch("api.tasks.send_mailing")
    def test_send_mailing_success(
        self, send_mailing_mock, message_instance_one
    ):
        assert message_instance_one.status == "SC"
        send_mailing_mock.return_value.status_code = 200
        send_mailing(message_instance_one.id)
        message_instance_one.refresh_from_db()
        assert message_instance_one.status == "DL"


def test_get_mailings_stats():
    queryset = [
        {"mailing_id": 1, "status": "SC", "message_count": 10},
        {"mailing_id": 1, "status": "DL", "message_count": 15},
        {"mailing_id": 2, "status": "SC", "message_count": 8},
        {"mailing_id": 2, "status": "ND", "message_count": 5},
    ]
    res = get_mailings_stats(queryset)
    exp = {
        1: {"SC": 10, "DL": 15},
        2: {"SC": 8, "ND": 5},
    }
    assert exp == res


@pytest.mark.django_db
class TestTaskManager:
    @freeze_time("01-01-2024")
    @patch("api.tasks.send_mailing.apply_async")
    @patch("api.models.Message.save")
    def test_create_message_celery_task(
        self, mock_save, mock_send_mailing_apply_async, message_instance_one
    ):
        mock_send_mailing_apply_async.return_value.id = "mock_celery_task_id"
        TaskManager.create_message_celery_task(message_instance_one)
        mock_send_mailing_apply_async.assert_called_once_with(
            args=[message_instance_one.id],
            eta=dt(2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC),
        )
        assert message_instance_one.celery_task_id == "mock_celery_task_id"
        mock_save.assert_called_once()

    @patch("api.tasks.current_app.control.revoke")
    @patch("api.models.Message.save")
    @patch("api.tasks.current_app.AsyncResult")
    def test_delete_message_celery_task(
        self, mock_async_result, mock_save, mock_revoke, message_instance_one
    ):
        message_instance_one.celery_task_id = "mock_celery_task_id"
        TaskManager.delete_message_celery_task(message_instance_one)
        mock_async_result.assert_called_once_with("mock_celery_task_id")
        mock_revoke.assert_called_once_with(
            "mock_celery_task_id", terminate=True
        )
        assert message_instance_one.status == Message.Status.CANCELLED
        mock_save.assert_called_once()

    @patch("api.tasks.TaskManager.delete_message_celery_task")
    @patch("api.tasks.TaskManager.create_new_message_and_send")
    def test_update_message_celery_task(
        self, mock_create_new_task, mock_delete_task, message_instance_one
    ):
        TaskManager.update_message_celery_task(message_instance_one)
        mock_delete_task.assert_called_once_with(message_instance_one)
        mock_create_new_task.assert_called_once_with(message_instance_one)

    @freeze_time("2024-01-02 12:00:00", tz_offset=0)
    @patch("api.tasks.send_mailing.apply_async")
    def test_create_new_message_and_send(
        self, mock_apply_async, message_instance_one
    ):
        mock_apply_async.return_value.id = "mock_celery_task_id"
        TaskManager.create_new_message_and_send(message_instance_one)
        new_message = Message.objects.get(id=2)
        assert new_message.client == message_instance_one.client
        assert new_message.mailing == message_instance_one.mailing
        mock_apply_async.assert_called_once_with(
            args=[2],
            eta=dt(2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC),
        )
