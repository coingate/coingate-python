from typing import List, Optional


class ApiException(Exception):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        self.reason = reason
        self.status_code = status_code
        self.message = message
        self.errors = errors

        super().__init__()

    def __str__(self) -> str:
        errors = self._join_errors()
        return f"(status_code={self.status_code}, reason={self.reason}, message={self.message}, errors={errors})"

    def _join_errors(self) -> Optional[str]:
        return ", ".join(self.errors) if self.errors is not None else None


class AbstractClientException(ApiException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)

    def __str__(self) -> str:
        errors = self._join_errors()
        return f'(message="{self.message}", errors="{errors}")'


class BadCredentialsException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class BadAuthTokenException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class PageNotFoundException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class RecordNotFoundException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class InternalServerErrorException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class RateLimitException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class OrderIsNotValidException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class OrderNotFoundException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class RefundIsNotValidException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class RefundNotFoundException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class LedgerAccountNotFoundException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)


class WithdrawalNotFoundException(AbstractClientException):
    def __init__(
        self,
        reason: str,
        status_code: int,
        message: Optional[str],
        errors: Optional[List[str]],
    ) -> None:
        super().__init__(reason, status_code, message, errors)
