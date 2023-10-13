from fastapi.exceptions import HTTPException


class JWTException(HTTPException):
    def __init__(self, error="invalid_token") -> None:
        super().__init__(
            status_code=401,
            detail={"error": error},
            headers={"WWW-Authenticate": "Bearer"},
        )


class AlreadyExists(HTTPException):
    def __init__(self, error="already_exists") -> None:
        super().__init__(status_code=400, detail={"error": error})


class DoesntExists(HTTPException):
    def __init__(self, error="doesnt_exists") -> None:
        super().__init__(status_code=400, detail={"error": error})
