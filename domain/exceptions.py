class DuplicateRequestError(Exception):
    """Raised when a request ID already exists."""


class RequestNotFoundError(Exception):
    """Raised when a request cannot be found."""


class InvalidPriorityError(Exception):
    """Raised when a priority is not LOW, MEDIUM, or HIGH."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""


class AuthorizationError(Exception):
    """Raised when a user lacks permission for an operation."""


class AlreadyResolvedError(Exception):
    """Raised when an already resolved request is resolved again."""


class InvalidMenuChoiceError(Exception):
    """Raised for an invalid menu choice."""


class RepositoryError(Exception):
    """Raised when repository storage cannot be read or written safely."""
