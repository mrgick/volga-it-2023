from fastapi.exceptions import HTTPException


class JWTException(HTTPException):
    def __init__(self, error="invalid_token") -> None:
        super().__init__(
            status_code=401,
            detail={"error": error},
            headers={"WWW-Authenticate": "Bearer"},
        )


class BadRequest(HTTPException):
    def __init__(self, error="bad_request") -> None:
        super().__init__(status_code=400, detail={"error": error})


class AlreadyExists(HTTPException):
    def __init__(self, error="already_exists") -> None:
        super().__init__(status_code=400, detail={"error": error})


class NotFound(HTTPException):
    def __init__(self, error="not_found") -> None:
        super().__init__(status_code=404, detail={"error": error})
