import json
import logging
from urllib.parse import unquote

logger = logging.getLogger("api")


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/metrics":
            response = self.get_response(request)
            return response
        self.log_request(request)
        response = self.get_response(request)
        self.log_response(response)
        return response

    def log_request(self, request):
        body = None
        if request.content_type == "application/json":
            try:
                body = request.data
            except AttributeError:
                body = request.body.decode("utf-8")
        elif request.content_type == "application/x-www-form-urlencoded":
            json_data = {
                key: unquote(value) for key, value in request.POST.items()
            }
            body = json.dumps(json_data, indent=2)

        logger.info(
            f"API Request: {request.method} {request.path}, "
            f"Body: {body}, "
            f"Headers: {request.headers}"
        )

    def log_response(self, response):
        try:
            body = response.data
        except AttributeError:
            body = None

        logger.info(
            f"API Response: Status Code: {response.status_code}, "
            f"Body: {body}, "
            f"Headers: {response.headers}"
        )
