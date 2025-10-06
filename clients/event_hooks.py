import allure
from httpx import Request, Response

from utils.http.curl import make_curl_from_request
from utils.logger import get_logger

logger = get_logger("HTTP_CLIENT")


def curl_attach_to_allure_event_hook(request: Request):
    curl = make_curl_from_request(request)
    allure.attach(curl, "cURL command", allure.attachment_type.TEXT)


def log_request_event_hook(request: Request):
    logger.info(f'Make {request.method} request to {request.url}')


def log_response_event_hook(response: Response):
    logger.info(
        f"Got response {response.status_code} {response.reason_phrase} from {response.url}"
    )