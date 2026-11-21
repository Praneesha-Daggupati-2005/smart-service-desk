import tempfile
import unittest
from pathlib import Path

from application.request_service import RequestService
from infrastructure.file_repository import FileRepository
from domain.exceptions import (
    DuplicateRequestError,
    RequestNotFoundError,
    InvalidPriorityError,
    AuthorizationError,
    AlreadyResolvedError,
)


class TestRequestService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repository = FileRepository(Path(self.temp_dir.name) / "requests.json")
        self.service = RequestService(self.repository)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_successful_creation(self):
        request = self.service.create_request("SR101", "Rahul", "Laptop issue", "HIGH", "employee")
        self.assertEqual(request.status, "OPEN")

    def test_duplicate_rejection(self):
        self.service.create_request("SR101", "Rahul", "Laptop issue", "HIGH", "employee")
        with self.assertRaises(DuplicateRequestError):
            self.service.create_request("SR101", "Priya", "Wi-Fi issue", "LOW", "employee")

    def test_priority_validation(self):
        with self.assertRaises(InvalidPriorityError):
            self.service.create_request("SR102", "Rahul", "Laptop issue", "URGENT", "employee")

    def test_search_existing_request(self):
        self.service.create_request("SR103", "Rahul", "Laptop issue", "MEDIUM", "employee")
        request = self.service.search_request("SR103")
        self.assertEqual(request.request_id, "SR103")

    def test_search_missing_request(self):
        with self.assertRaises(RequestNotFoundError):
            self.service.search_request("SR999")

    def test_employee_resolution_rejected(self):
        self.service.create_request("SR104", "Rahul", "Laptop issue", "HIGH", "employee")
        with self.assertRaises(AuthorizationError):
            self.service.resolve_request("SR104", "employee", "EMPLOYEE")

    def test_admin_resolution_allowed(self):
        self.service.create_request("SR105", "Rahul", "Laptop issue", "HIGH", "employee")
        request = self.service.resolve_request("SR105", "admin", "ADMIN")
        self.assertEqual(request.status, "RESOLVED")

    def test_already_resolved_rejected(self):
        self.service.create_request("SR106", "Rahul", "Laptop issue", "LOW", "employee")
        self.service.resolve_request("SR106", "admin", "ADMIN")
        with self.assertRaises(AlreadyResolvedError):
            self.service.resolve_request("SR106", "admin", "ADMIN")

    def test_view_all_requests(self):
        self.service.create_request("SR107", "Rahul", "Laptop issue", "HIGH", "employee")
        self.service.create_request("SR108", "Priya", "Wi-Fi issue", "MEDIUM", "employee2")
        self.assertEqual(len(self.service.view_requests()), 2)

    def test_view_only_logged_in_employee_requests(self):
        self.service.create_request("SR109", "Rahul", "Laptop issue", "HIGH", "employee")
        self.service.create_request("SR110", "Priya", "Wi-Fi issue", "MEDIUM", "employee2")
        mine = self.service.view_my_requests("employee")
        self.assertEqual(len(mine), 1)
        self.assertEqual(mine[0].created_by, "employee")


if __name__ == "__main__":
    unittest.main()
