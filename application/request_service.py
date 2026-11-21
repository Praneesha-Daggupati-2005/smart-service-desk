from domain.service_request import ServiceRequest
from domain.exceptions import (
    DuplicateRequestError,
    RequestNotFoundError,
    InvalidPriorityError,
    AuthorizationError,
    AlreadyResolvedError,
)


class RequestService:
    """Application use cases; depends on the repository abstraction."""

    def __init__(self, repository):
        self.repository = repository

    def create_request(self, request_id, employee_name, issue, priority, username):
        if self.repository.find_by_id(request_id):
            raise DuplicateRequestError("A request with this Request ID already exists.")

        request = ServiceRequest(
            request_id=request_id,
            employee_name=employee_name,
            issue=issue,
            priority=priority,
            status="OPEN",
            created_by=username,
        )
        self.repository.add(request)
        return request

    def view_requests(self):
        return self.repository.get_all()

    def search_request(self, request_id):
        request = self.repository.find_by_id(request_id)
        if request is None:
            raise RequestNotFoundError("Request not found.")
        return request

    def resolve_request(self, request_id, username, role):
        if role != "ADMIN":
            raise AuthorizationError("Only ADMIN users can resolve requests.")

        request = self.repository.find_by_id(request_id)
        if request is None:
            raise RequestNotFoundError("Request not found.")

        request.resolve()
        self.repository.update(request)
        return request

    def view_my_requests(self, username):
        return [
            request
            for request in self.repository.get_all()
            if request.created_by == username
        ]
