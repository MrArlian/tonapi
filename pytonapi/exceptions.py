import typing as t

__all__ = [
    "STREAMING_RECOVERABLE",
    "TONAPI_STATUS_TO_EXCEPTION",
    "TONAPIBadRequestError",
    "TONAPIClientError",
    "TONAPIConflictError",
    "TONAPIConnectionError",
    "TONAPIConnectionLostError",
    "TONAPIError",
    "TONAPIForbiddenError",
    "TONAPIGatewayTimeoutError",
    "TONAPIInternalServerError",
    "TONAPIMethodNotAllowedError",
    "TONAPINotFoundError",
    "TONAPINotImplementedError",
    "TONAPIRetryLimitError",
    "TONAPIServerError",
    "TONAPISessionNotCreatedError",
    "TONAPIStatusError",
    "TONAPIStreamingError",
    "TONAPITooManyRequestsError",
    "TONAPIUnauthorizedError",
    "TONAPIUnprocessableError",
    "TONAPIValidationError",
    "raise_for_status",
]


class TONAPIError(Exception):
    """Base exception for all TONAPI errors."""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class TONAPIConnectionError(TONAPIError):
    """Network-level error (DNS failure, timeout, refused connection)."""


class TONAPIStatusError(TONAPIError):
    """API returned a non-2xx HTTP status."""

    status: int
    hint: t.ClassVar[str] = ""

    def __init__(self, *, status: int, message: str) -> None:
        self.status = status
        text = f"HTTP {status}: {message}"
        if self.hint:
            text += f" — {self.hint}"
        super().__init__(text)


class TONAPIClientError(TONAPIStatusError):
    """Client-side HTTP error (4xx)."""


class TONAPIServerError(TONAPIStatusError):
    """Server-side HTTP error (5xx)."""


class TONAPIBadRequestError(TONAPIClientError):
    """HTTP 400 Bad Request."""

    hint = "check query parameters, request body, and path arguments"


class TONAPIUnauthorizedError(TONAPIClientError):
    """HTTP 401 Unauthorized."""

    hint = "get a valid API key at https://tonconsole.com/"


class TONAPIForbiddenError(TONAPIClientError):
    """HTTP 403 Forbidden."""

    hint = "check your API key permissions at https://tonconsole.com/"


class TONAPINotFoundError(TONAPIClientError):
    """HTTP 404 Not Found."""


class TONAPIMethodNotAllowedError(TONAPIClientError):
    """HTTP 405 Method Not Allowed."""


class TONAPIConflictError(TONAPIClientError):
    """HTTP 409 Conflict."""


class TONAPIUnprocessableError(TONAPIClientError):
    """HTTP 422 Unprocessable Entity."""


class TONAPITooManyRequestsError(TONAPIClientError):
    """HTTP 429 Too Many Requests."""

    hint = "reduce request frequency or upgrade your plan at https://tonconsole.com/"


class TONAPIInternalServerError(TONAPIServerError):
    """HTTP 500 Internal Server Error."""


class TONAPINotImplementedError(TONAPIServerError):
    """HTTP 501 Not Implemented."""


class TONAPIGatewayTimeoutError(TONAPIServerError):
    """HTTP 504 Gateway Timeout."""


class TONAPIValidationError(TONAPIError):
    """Response body did not match the expected Pydantic model."""

    model: type
    errors: list[t.Any]

    def __init__(self, *, model: type, errors: list[t.Any]) -> None:
        self.model = model
        self.errors = errors
        field_hints = ", ".join(f"{e.get('loc', '?')}: {e.get('msg', '')}" for e in errors[:3])
        if len(errors) > 3:
            field_hints += f" ... (+{len(errors) - 3} more)"
        super().__init__(
            f"Response validation failed for {model.__name__}: {field_hints}",
        )


class TONAPIStreamingError(TONAPIError):
    """Streaming transport error."""


class TONAPIConnectionLostError(TONAPIStreamingError):
    """Connection lost and reconnect limit exceeded."""

    attempts: int

    def __init__(self, *, attempts: int) -> None:
        self.attempts = attempts
        super().__init__(
            f"Connection lost after {attempts} reconnect attempts",
        )


class TONAPISessionNotCreatedError(TONAPIError):
    """Session was not created before making a request."""

    def __init__(self, client_name: str) -> None:
        super().__init__(
            f"Session is not created. "
            f"Call 'await {client_name}(...).create_session()' "
            f"or use 'async with {client_name}(...) as client:'"
        )


class TONAPIRetryLimitError(TONAPIError):
    """All retry attempts have been exhausted."""

    attempts: int
    last_status: int | None
    last_error: Exception | None

    def __init__(
        self,
        *,
        attempts: int,
        last_status: int | None = None,
        last_error: Exception | None = None,
    ) -> None:
        self.attempts = attempts
        self.last_status = last_status
        self.last_error = last_error
        parts = [f"Retry limit exceeded after {attempts} attempts"]
        if last_status is not None:
            parts.append(f"last status: {last_status}")
        if last_error is not None:
            parts.append(f"last error: {last_error}")
        super().__init__(", ".join(parts))


STREAMING_RECOVERABLE: t.Final[tuple[type[TONAPIError], ...]] = (
    TONAPIServerError,
    TONAPITooManyRequestsError,
    TONAPIStreamingError,
)

TONAPI_STATUS_TO_EXCEPTION: t.Final[dict[int, type[TONAPIStatusError]]] = {
    400: TONAPIBadRequestError,
    401: TONAPIUnauthorizedError,
    403: TONAPIForbiddenError,
    404: TONAPINotFoundError,
    405: TONAPIMethodNotAllowedError,
    409: TONAPIConflictError,
    422: TONAPIUnprocessableError,
    429: TONAPITooManyRequestsError,
    500: TONAPIInternalServerError,
    501: TONAPINotImplementedError,
    504: TONAPIGatewayTimeoutError,
}


def raise_for_status(status: int, body: str, content_type: str = "") -> None:
    """Raise an appropriate exception for non-2xx HTTP status.

    :param status: HTTP status code.
    :param body: Response body text.
    :param content_type: Content-Type header value.
    :raises TONAPIStatusError: On any mapped HTTP error.
    """
    import json

    if "text/html" in content_type:
        message = "Unexpected HTML response"
    else:
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            message = body
        else:
            if isinstance(data, dict):
                message = data.get("error") or data.get("Error") or body
                if isinstance(message, dict):
                    message = str(message)
            else:
                message = str(data)

    exc_class = TONAPI_STATUS_TO_EXCEPTION.get(status)
    if exc_class:
        raise exc_class(status=status, message=message)

    if 400 <= status < 500:
        raise TONAPIClientError(status=status, message=message)
    if 500 <= status < 600:
        raise TONAPIServerError(status=status, message=message)

    raise TONAPIError(f"HTTP {status}: {message}")
