from pathlib import Path

from infrastructure.file_repository import FileRepository
from presentation.auth import AuthenticationService
from presentation.main_app import MainApplication


BASE_DIR = Path(__file__).resolve().parent


if __name__ == "__main__":
    repository = FileRepository(BASE_DIR / "data" / "requests.json")
    auth_service = AuthenticationService(BASE_DIR / "data" / "users.json")
    app = MainApplication(repository, auth_service)
    app.run()
