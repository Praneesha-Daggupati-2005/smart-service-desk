import hashlib
import json
import secrets
from pathlib import Path

from domain.exceptions import InvalidCredentialsError, RepositoryError


class AuthenticationService:
    """Loads users and verifies salted PBKDF2 password hashes."""

    def __init__(self, users_file):
        self.users_file = Path(users_file)

    @staticmethod
    def hash_password(password, salt=None):
        if isinstance(salt, bytes):
            salt_bytes = salt
        elif isinstance(salt, str):
            try:
                salt_bytes = bytes.fromhex(salt)
            except ValueError:
                salt_bytes = salt.encode("utf-8")
        else:
            salt_bytes = secrets.token_bytes(16)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 120000)
        return "pbkdf2_sha256", salt_bytes.hex(), derived.hex()

    def _load_users(self):
        if not self.users_file.exists():
            raise RepositoryError("User account file is missing.")
        try:
            if self.users_file.stat().st_size == 0:
                return []
            with self.users_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise RepositoryError("The user account JSON file is corrupted.") from exc
        except OSError as exc:
            raise RepositoryError("The user account file could not be read.") from exc
        if not isinstance(data, list):
            raise RepositoryError("The user account JSON must contain a list.")
        return data

    def authenticate(self, username, password):
        for user in self._load_users():
            if user.get("username") == username:
                if user.get("algorithm") != "pbkdf2_sha256":
                    break
                salt = bytes.fromhex(user["salt"])
                _, _, derived = self.hash_password(password, salt)
                if secrets.compare_digest(derived, user["password_hash"]):
                    role = str(user.get("role", "EMPLOYEE")).upper()
                    if role not in {"ADMIN", "EMPLOYEE"}:
                        raise InvalidCredentialsError("Invalid username or password.")
                    return {"username": username, "role": role}
                break
        raise InvalidCredentialsError("Invalid username or password.")
