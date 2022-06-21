import respx
import pytest
import httpx

import random

def _reflect_request(request: httpx.Request) -> respx.MockResponse:
    reflect_headers = {"content-type", "content-length"}
    headers = {k: v for (k, v) in request.headers.items() if k in reflect_headers}
    return respx.MockResponse(200, content=request.content, headers=headers)


def _reflect_request_random_status(request: httpx.Request) -> respx.MockResponse:
    response = _reflect_request(request)
    response.status_code = random.choice((200, 200, 201, 202, 401, 403, 404, 422, 500))
    return response


@pytest.fixture
def http_reflect():
    """Return all outgoing http POST | PUT | PATCH request's payload as a response."""
    # TODO: make http_reflect_airgap
    # pylint: disable=not-context-manager
    with respx.mock(assert_all_called=False, assert_all_mocked=True) as respx_mock:

        respx_mock.route(method__in=["POST", "PUT", "PATCH"]).mock(
            side_effect=_reflect_request
        )

        yield respx_mock


@pytest.fixture
def http_reflect_random_status():
    """Randomize status codes. Return all outgoing http request's payload as a response."""
    # pylint: disable=not-context-manager
    with respx.mock(assert_all_called=False, assert_all_mocked=True) as respx_mock:

        respx_mock.route(method__in=["POST", "PUT", "PATCH"]).mock(
            side_effect=_reflect_request_random_status
        )

        yield respx_mock