import unittest

from domain.service_request import ServiceRequest
from domain.exceptions import InvalidPriorityError, AlreadyResolvedError


class TestServiceRequest(unittest.TestCase):
    def test_default_status_is_open(self):
        request = ServiceRequest("SR101", "Rahul", "Laptop issue", "HIGH")
        self.assertEqual(request.status, "OPEN")

    def test_priority_validation(self):
        with self.assertRaises(InvalidPriorityError):
            ServiceRequest("SR102", "Rahul", "Laptop issue", "URGENT")

    def test_resolve_open_request(self):
        request = ServiceRequest("SR103", "Rahul", "Laptop issue", "MEDIUM")
        request.resolve()
        self.assertEqual(request.status, "RESOLVED")

    def test_resolve_again_rejected(self):
        request = ServiceRequest("SR104", "Rahul", "Laptop issue", "LOW")
        request.resolve()
        with self.assertRaises(AlreadyResolvedError):
            request.resolve()


if __name__ == "__main__":
    unittest.main()
