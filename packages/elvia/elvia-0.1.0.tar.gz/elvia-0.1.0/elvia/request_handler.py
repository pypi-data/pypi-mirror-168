from elvia.error import (
    InvalidRequestBody,
    AuthError,
    UnexpectedError,
)


async def verify_response(response, expected_status):
    if response.status == 400:
        raise InvalidRequestBody(
            "Body is malformed",
            status_code=response.status,
            headers=response.headers,
            body=await response.text(),
        )

    if response.status in [401, 403]:
        raise AuthError(
            "Auth failed",
            status_code=response.status,
            headers=response.headers,
            body=await response.text(),
        )

    if response.status != expected_status:
        raise UnexpectedError(
            "Received unexpected server response",
            status_code=response.status,
            headers=response.headers,
            body=await response.text(),
        )
