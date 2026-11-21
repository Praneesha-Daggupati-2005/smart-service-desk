import json
import tempfile
import unittest
from pathlib import Path

from domain.service_request import ServiceRequest
from infrastructure.file_repository import FileRepository
from domain.exceptions import RepositoryError


class TestFileRepository(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "requests.json"
        self.repository = FileRepository(self.path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_reload(self):
        request = ServiceRequest("SR101", "Rahul", "Laptop issue", "HIGH")
        self.repository.add(request)
        reloaded = FileRepository(self.path).get_all()
        self.assertEqual(reloaded[0].request_id, "SR101")

    def test_missing_file_handling(self):
        self.assertEqual(self.repository.get_all(), [])

    def test_empty_file_handling(self):
        self.path.write_text("", encoding="utf-8")
        self.assertEqual(self.repository.get_all(), [])

    def test_bom_with_empty_json_list(self):
        self.path.write_bytes(b"\xef\xbb\xbf[]")
        self.assertEqual(self.repository.get_all(), [])

    def test_corrupted_json_handling(self):
        self.path.write_text("{bad json", encoding="utf-8")
        with self.assertRaises(RepositoryError):
            self.repository.get_all()


if __name__ == "__main__":
    unittest.main()
