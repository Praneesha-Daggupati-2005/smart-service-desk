"""Domain layer for Smart Service Desk."""

from .service_request import ServiceRequest
from .exceptions import (
    DuplicateRequestError,
    RequestNotFoundError,
    InvalidPriorityError,
    InvalidCredentialsError,
    AuthorizationError,
    AlreadyResolvedError,
    InvalidMenuChoiceError,
    RepositoryError,
)

__all__ = [
    "ServiceRequest",
    "DuplicateRequestError",
    "RequestNotFoundError",
    "InvalidPriorityError",
    "InvalidCredentialsError",
    "AuthorizationError",
    "AlreadyResolvedError",
    "InvalidMenuChoiceError",
    "RepositoryError",
]
