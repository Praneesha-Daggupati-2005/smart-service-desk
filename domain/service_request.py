from .exceptions import InvalidPriorityError, AlreadyResolvedError


class ServiceRequest:
    """Domain entity representing an IT support service request."""

    ALLOWED_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}
    ALLOWED_STATUSES = {"OPEN", "RESOLVED"}

    def __init__(
        self,
        request_id,
        employee_name,
        issue,
        priority,
        status="OPEN",
        created_by=None,
    ):
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("Request ID is required.")
        if not isinstance(employee_name, str) or not employee_name.strip():
            raise ValueError("Employee name is required.")
        if not isinstance(issue, str) or not issue.strip():
            raise ValueError("Issue description is required.")

        normalized_priority = str(priority).strip().upper()
        if normalized_priority not in self.ALLOWED_PRIORITIES:
            raise InvalidPriorityError(
                "Priority must be LOW, MEDIUM or HIGH."
            )

        normalized_status = str(status).strip().upper()
        if normalized_status not in self.ALLOWED_STATUSES:
            raise ValueError("Status must be OPEN or RESOLVED.")

        self.__request_id = request_id.strip()
        self.__employee_name = employee_name.strip()
        self.__issue = issue.strip()
        self.__priority = normalized_priority
        self.__status = normalized_status
        self.__created_by = created_by

    @property
    def request_id(self):
        return self.__request_id

    @property
    def employee_name(self):
        return self.__employee_name

    @property
    def issue(self):
        return self.__issue

    @property
    def priority(self):
        return self.__priority

    @property
    def status(self):
        return self.__status

    @property
    def created_by(self):
        return self.__created_by

    def resolve(self):
        if self.__status == "RESOLVED":
            raise AlreadyResolvedError("Request is already resolved.")
        self.__status = "RESOLVED"

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Request JSON entry must be an object.")
        return cls(
            request_id=data.get("request_id"),
            employee_name=data.get("employee_name"),
            issue=data.get("issue"),
            priority=data.get("priority"),
            status=data.get("status", "OPEN"),
            created_by=data.get("created_by"),
        )
