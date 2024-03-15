# SMS-Sender

Service for managing SMS mailings.


### Description

The service launches mailings to a client list based on predefined rules.

The API includes endpoints for:

- managing clients (adding, editing, deleting)

- managing mailings (adding, editing, deleting, retrieving statistics - both
  overall and per each mailing)

For integration with other projects, there is an external service with its own
API.

### Technologies

1. Django совместно с Django-Rest-Framework
   
2. RabbitMQ
   
3. Celery
   
4. PostgreSQL


### To deploy the project locally, follow these main steps:


1. Clone the project

```shell
git clone git@github.com:maskalev/sms-sender.git
```

1. Create .env file in root directory of the project:
   
    - `SECRET_KEY` - Django app's secret key

    - `API_URL` - URL of an external service API

    - `API_TOKEN` - token for accessing to an external service API

    - `DB_ENGINE` - database engine

    - `DB_NAME` - database name

    - `DB_USER` - database user

    - `DB_PASSWORD` - database user's password

    - `DB_HOST` - database host

    - `DB_PORT` - database port


3. Run the project
   
```shell
sudo docker compose up -d --build
```

4. Create and make migrations
   
```shell
sudo docker compose exec -T app python3 manage.py makemigrations api --no-input
sudo docker compose exec -T app python3 manage.py migrate --no-input
```

5. Collect static
   
```shell
sudo docker compose exec -T app python3 manage.py collectstatic --no-input
```

6. Restart the project
   
```shell
sudo docker compose restart
```

7. Copy data (if it needs)
   
```shell
sudo docker compose exec -T app python manage.py loaddata fixtures.json
```

The service is available on *localhost/api/v1/*.

API docs available on *localhost/docs/*.

Superuser's creditionals (if you use fixtures): *admin/admin*.

### Requests examples

#### Clients

To create a client

```shell
curl -X POST http://localhost:8000/api/v1/clients/ -H 'Content-Type: application/json' -d '{"phone": "71230000001"}'
```

```json
{
    "id": 1,
    "phone": "71230000001",
    "operator_code": "123",
    "tag": null,
    "time_zone": "UTC",
    "created_at": "2024-02-14T08:42:49.704376Z",
    "updated_at": "2024-02-14T08:42:49.704405Z"
}
```

To edit the client

```shell
curl -X PATCH http://localhost:8000/api/v1/clients/1/ -H 'Content-Type: application/json' -d '{"time_zone": "Europe/Moscow"}'
```

```json
{
    "id": 1,
    "phone": "71230000001",
    "operator_code": "123",
    "tag": null,
    "time_zone": "Europe/Moscow",
    "created_at": "2024-02-14T08:42:49.704376Z",
    "updated_at": "2024-02-14T08:44:59.111742Z"
}
```

To get client's data

```shell
curl http://localhost:8000/api/v1/clients/1/
```

```json
{
    "id": 1,
    "phone": "71230000001",
    "operator_code": "123",
    "tag": null,
    "time_zone": "Europe/Moscow",
    "created_at": "2024-02-14T08:42:49.704376Z",
    "updated_at": "2024-02-14T08:44:59.111742Z"
}
```

To get list ot the clients

```shell
curl http://localhost:8000/api/v1/clients/
```

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "phone": "71230000001",
            "operator_code": "123",
            "tag": null,
            "time_zone": "Europe/Moscow",
            "created_at": "2024-02-14T08:42:49.704376Z",
            "updated_at": "2024-02-14T08:44:59.111742Z"
        },
        {
            "id": 2,
            "phone": "71230000002",
            "operator_code": "123",
            "tag": null,
            "time_zone": "UTC",
            "created_at": "2024-02-14T08:45:30.556096Z",
            "updated_at": "2024-02-14T08:45:30.556111Z"
        },
        {
            "id": 3,
            "phone": "71230000003",
            "operator_code": "123",
            "tag": null,
            "time_zone": "UTC",
            "created_at": "2024-02-14T08:45:34.457324Z",
            "updated_at": "2024-02-14T08:45:34.457354Z"
        }
    ]
}
```

To remove the client

```shell
curl -X DELETE http://localhost:8000/api/v1/clients/1/
```

```json
```

#### Mailings

To create a mailing

```shell
curl -X POST http://localhost:8000/api/v1/mailings/ -H 'Content-Type: application/json' -d '{"datetime_start": "2024-02-12T12:14:00Z", "datetime_end": "2024-03-11T20:15:00Z", "text": "Some text"}'
```

```json
{
    "id": 1,
    "datetime_start": "2024-02-12T12:14:00Z",
    "datetime_end": "2024-03-11T20:15:00Z",
    "send_interval_time_start": null,
    "send_interval_time_end": null,
    "text": "Some text",
    "client_filter": null,
    "clients_count": 0,
    "scheduled_messages": 0,
    "created_messages": 0,
    "delivered_messages": 0,
    "undelivered_messages": 0,
    "cancelled_messages": 0,
    "created_at": "2024-02-14T08:47:43.458076Z",
    "updated_at": "2024-02-14T08:47:43.458082Z"
}
```

To get mailing's data

```shell
curl http://localhost:8000/api/v1/mailings/1/
```

```json
{
    "id": 1,
    "datetime_start": "2024-02-12T12:14:00Z",
    "datetime_end": "2024-03-11T20:15:00Z",
    "send_interval_time_start": null,
    "send_interval_time_end": null,
    "text": "Some text",
    "client_filter": null,
    "clients_count": 3,
    "scheduled_messages": 0,
    "created_messages": 3,
    "delivered_messages": 3,
    "undelivered_messages": 0,
    "cancelled_messages": 0,
    "created_at": "2024-02-14T08:47:43.458076Z",
    "updated_at": "2024-02-14T08:47:43.458082Z",
    "mailing_messages": [
        {
            "id": 3,
            "datetime_send": "2024-02-14T08:47:43.474183Z",
            "status": "DL",
            "mailing_id": 1,
            "client_id": 3,
            "celery_task_id": "0e088ef0-b877-45e2-910f-9eab432b3985",
            "created_at": "2024-02-14T08:47:43.474215Z",
            "updated_at": "2024-02-14T08:47:43.474219Z"
        },
        {
            "id": 2,
            "datetime_send": "2024-02-14T08:47:43.470083Z",
            "status": "DL",
            "mailing_id": 1,
            "client_id": 2,
            "celery_task_id": "b48c3a08-46fb-47ac-804d-e93bc989bdef",
            "created_at": "2024-02-14T08:47:43.470108Z",
            "updated_at": "2024-02-14T08:47:43.470111Z"
        },
        {
            "id": 1,
            "datetime_send": "2024-02-14T08:47:43.463026Z",
            "status": "DL",
            "mailing_id": 1,
            "client_id": 1,
            "celery_task_id": "5ac55c54-c79d-4c71-b89d-c903be7921a0",
            "created_at": "2024-02-14T08:47:43.463054Z",
            "updated_at": "2024-02-14T08:47:43.463058Z"
        }
    ]
}
```

To get the list of the mailings

```shell
curl http://localhost:8000/api/v1/mailings/
```

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "datetime_start": "2024-02-12T12:14:00Z",
            "datetime_end": "2024-03-11T20:15:00Z",
            "send_interval_time_start": null,
            "send_interval_time_end": null,
            "text": "Some text",
            "client_filter": null,
            "clients_count": 3,
            "scheduled_messages": 0,
            "created_messages": 3,
            "delivered_messages": 3,
            "undelivered_messages": 0,
            "cancelled_messages": 0,
            "created_at": "2024-02-14T08:47:43.458076Z",
            "updated_at": "2024-02-14T08:47:43.458082Z"
        },
        {
            "id": 2,
            "datetime_start": "2024-02-12T12:14:00Z",
            "datetime_end": "2024-03-12T20:15:00Z",
            "send_interval_time_start": null,
            "send_interval_time_end": null,
            "text": "Text",
            "client_filter": null,
            "clients_count": 3,
            "scheduled_messages": 0,
            "created_messages": 3,
            "delivered_messages": 3,
            "undelivered_messages": 0,
            "cancelled_messages": 0,
            "created_at": "2024-02-14T08:48:46.213404Z",
            "updated_at": "2024-02-14T08:48:46.213410Z"
        },
        {
            "id": 3,
            "datetime_start": "2024-03-12T12:14:00Z",
            "datetime_end": "2024-03-12T20:15:00Z",
            "send_interval_time_start": null,
            "send_interval_time_end": null,
            "text": "Text",
            "client_filter": null,
            "clients_count": 3,
            "scheduled_messages": 3,
            "created_messages": 3,
            "delivered_messages": 0,
            "undelivered_messages": 0,
            "cancelled_messages": 0,
            "created_at": "2024-02-14T08:49:17.021904Z",
            "updated_at": "2024-02-14T08:49:17.021909Z"
        }
    ]
}
```

To edit the mailing

```shell
curl -X PATCH http://localhost:8000/api/v1/mailings/1/ -H 'Content-Type: application/json' -d '{"client_filter": "123, tag"}'
```

```json
{
    "id": 3,
    "datetime_start": "2024-03-12T12:14:00Z",
    "datetime_end": "2024-03-12T20:15:00Z",
    "send_interval_time_start": null,
    "send_interval_time_end": null,
    "text": "Text",
    "client_filter": "123",
    "clients_count": 3,
    "scheduled_messages": 3,
    "created_messages": 3,
    "delivered_messages": 0,
    "undelivered_messages": 0,
    "cancelled_messages": 0,
    "created_at": "2024-02-14T08:49:17.021904Z",
    "updated_at": "2024-02-14T09:10:16.447850Z"
}
```

To remove the mailing

```shell
curl -X DELETE http://localhost:8000/api/v1/mailings/3/
```

```json
```

### Additionally

1. Code testing is organized

    Testing is triggered with every commit. To manually run the tests, execute
    the command `pytest .`.

2. Docker-compose prepared to launch all project services with a single
   command

    To start, execute the command make deploy.

3. API docs is available on *localhost/docs/*.

4. An administrative Web UI has been implemented for managing mailings and
   obtaining statistics on sent messages.

5. Integration with an external [OAuth2](https://auth0.com) authorization
   service has been provided for the administrative interface.
   
   In the .env file, the following variables are required:

   `AUTH0_DOMAIN` - value from Domain field on OAuth2 servise. 

   `AUTH0_CLIENT_ID` - value from Client ID field on OAuth2 servise.

   `AUTH0_CLIENT_SECRET` - value from Client Secret on OAuth2 servise.

6. Implemented an additional service that sends statistics on processed
   mailings via email once a day.
   
   In the .env file, the following variables are required:

   `EMAIL_HOST` - email server's host
   
   `EMAIL_HOST_USER` - email user's login

   `EMAIL_HOST_PASSWORD` - email user's password

   `RECIPIENT_EMAIL_1`, `RECIPIENT_EMAIL_2` etc - recipients email addresses

7.  Prometheus metrics are exposed.

8.  Additional business logic has been implemented: "send_interval_time_start"
    and "send_interval_time_end" fields has been added to the "mailing" entity,
    allowing to specify a time range during which messages can be sent to
    clients based on their local time. Messages will not be sent to a client if
    their local time does not fall within the specified interval.

9.  Detailed logging is provided at every stage of request processing.

    Here is an example of logs related to the creation and sending of messages
    for a mailing:

   ```log
    2024-02-14 08:47:43,451 INFO middleware API Request: POST /api/v1/mailings/, Body: {"datetime_start": "2024-02-12T12:14:00Z", "datetime_end": "2024-03-11T20:15:00Z", "text": "Some text"}, Headers: {'Host': 'localhost:8000', 'User-Agent': 'curl/7.81.0', 'Accept': '*/*', 'Content-Type': 'application/json', 'Content-Length': '103'}
    2024-02-14 08:47:43,459 INFO signals Mailing_1 created. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f051684bf10>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 0, 'created_messages': 0, 'scheduled_messages': 0, 'delivered_messages': 0, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,462 INFO signals Mailing_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f051683b750>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=datetime.timezone.utc), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=datetime.timezone.utc), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 3, 'created_messages': 0, 'scheduled_messages': 0, 'delivered_messages': 0, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,469 INFO signals Mailing_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f051683b750>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=datetime.timezone.utc), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=datetime.timezone.utc), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 3, 'created_messages': 1, 'scheduled_messages': 1, 'delivered_messages': 0, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,469 INFO signals Message_1 created. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f051684a550>, 'id': 1, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 463026, tzinfo=datetime.timezone.utc), 'status': Message.Status.SCHEDULED, 'mailing_id': 1, 'client_id': 1, 'celery_task_id': None, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 463054, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 463058, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,473 INFO signals Mailing_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f051683b750>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=datetime.timezone.utc), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=datetime.timezone.utc), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 3, 'created_messages': 2, 'scheduled_messages': 2, 'delivered_messages': 0, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,473 INFO signals Message_2 created. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f0517925810>, 'id': 2, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 470083, tzinfo=datetime.timezone.utc), 'status': Message.Status.SCHEDULED, 'mailing_id': 1, 'client_id': 2, 'celery_task_id': None, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 470108, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 470111, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,477 INFO signals Mailing_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f051683b750>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=datetime.timezone.utc), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=datetime.timezone.utc), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 3, 'created_messages': 3, 'scheduled_messages': 3, 'delivered_messages': 0, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,478 INFO signals Message_3 created. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f05169681d0>, 'id': 3, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 474183, tzinfo=datetime.timezone.utc), 'status': Message.Status.SCHEDULED, 'mailing_id': 1, 'client_id': 3, 'celery_task_id': None, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 474215, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 474219, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,506 INFO signals Message_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f051684a550>, 'id': 1, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 463026, tzinfo=datetime.timezone.utc), 'status': Message.Status.SCHEDULED, 'mailing_id': 1, 'client_id': 1, 'celery_task_id': '5ac55c54-c79d-4c71-b89d-c903be7921a0', 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 463054, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 463058, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,508 INFO signals Message_2 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f0517925810>, 'id': 2, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 470083, tzinfo=datetime.timezone.utc), 'status': Message.Status.SCHEDULED, 'mailing_id': 1, 'client_id': 2, 'celery_task_id': 'b48c3a08-46fb-47ac-804d-e93bc989bdef', 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 470108, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 470111, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,511 INFO signals Message_3 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7f05169681d0>, 'id': 3, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 474183, tzinfo=datetime.timezone.utc), 'status': Message.Status.SCHEDULED, 'mailing_id': 1, 'client_id': 3, 'celery_task_id': '0e088ef0-b877-45e2-910f-9eab432b3985', 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 474215, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 474219, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:43,511 INFO middleware API Response: Status Code: 201, Body: {'id': 1, 'datetime_start': '2024-02-12T12:14:00Z', 'datetime_end': '2024-03-11T20:15:00Z', 'send_interval_time_start': None, 'send_interval_time_end': None, 'text': 'Some text', 'client_filter': None, 'clients_count': 0, 'scheduled_messages': 0, 'created_messages': 0, 'delivered_messages': 0, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': '2024-02-14T08:47:43.458076Z', 'updated_at': '2024-02-14T08:47:43.458082Z'}, Headers: {'Content-Type': 'application/json', 'Vary': 'Accept', 'Allow': 'GET, POST, HEAD, OPTIONS', 'X-Frame-Options': 'DENY', 'Content-Length': '407'}
    2024-02-14 08:47:44,047 INFO tasks Sending request to external service. Message_1 (Mailing_1) to Client_1
    2024-02-14 08:47:44,047 INFO tasks Message_1 (Mailing_1 to Client_1 was sent successfully. Status code: 200
    2024-02-14 08:47:44,067 INFO tasks Sending request to external service. Message_2 (Mailing_1) to Client_2
    2024-02-14 08:47:44,067 INFO tasks Sending request to external service. Message_3 (Mailing_1) to Client_3
    2024-02-14 08:47:44,068 INFO tasks Message_3 (Mailing_1 to Client_3 was sent successfully. Status code: 200
    2024-02-14 08:47:44,068 INFO tasks Message_2 (Mailing_1 to Client_2 was sent successfully. Status code: 200
    2024-02-14 08:47:44,072 INFO signals Mailing_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7fc54d3ec650>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=datetime.timezone.utc), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=datetime.timezone.utc), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 3, 'created_messages': 3, 'scheduled_messages': 2, 'delivered_messages': 1, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:44,072 INFO signals Message_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7fc54d2bf710>, 'id': 1, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 463026, tzinfo=datetime.timezone.utc), 'status': Message.Status.DELIVERED, 'mailing_id': 1, 'client_id': 1, 'celery_task_id': '5ac55c54-c79d-4c71-b89d-c903be7921a0', 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 463054, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 463058, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:44,078 INFO signals Mailing_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7fc54d3ec650>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=datetime.timezone.utc), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=datetime.timezone.utc), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 3, 'created_messages': 3, 'scheduled_messages': 0, 'delivered_messages': 3, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:44,079 INFO signals Message_3 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7fc54d3ec410>, 'id': 3, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 474183, tzinfo=datetime.timezone.utc), 'status': Message.Status.DELIVERED, 'mailing_id': 1, 'client_id': 3, 'celery_task_id': '0e088ef0-b877-45e2-910f-9eab432b3985', 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 474215, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 474219, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:44,079 INFO signals Mailing_1 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7fc54d3ec650>, 'id': 1, 'datetime_start': datetime.datetime(2024, 2, 12, 12, 14, tzinfo=datetime.timezone.utc), 'datetime_end': datetime.datetime(2024, 3, 11, 20, 15, tzinfo=datetime.timezone.utc), 'text': 'Some text', 'client_filter': None, 'send_interval_time_start': None, 'send_interval_time_end': None, 'clients_count': 3, 'created_messages': 3, 'scheduled_messages': 0, 'delivered_messages': 3, 'undelivered_messages': 0, 'cancelled_messages': 0, 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458076, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 458082, tzinfo=datetime.timezone.utc)}
    2024-02-14 08:47:44,079 INFO signals Message_2 updated. Attributes: {'_state': <django.db.models.base.ModelState object at 0x7fc54d2b5b10>, 'id': 2, 'datetime_send': datetime.datetime(2024, 2, 14, 8, 47, 43, 470083, tzinfo=datetime.timezone.utc), 'status': Message.Status.DELIVERED, 'mailing_id': 1, 'client_id': 2, 'celery_task_id': 'b48c3a08-46fb-47ac-804d-e93bc989bdef', 'created_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 470108, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 2, 14, 8, 47, 43, 470111, tzinfo=datetime.timezone.utc)}
   ```
