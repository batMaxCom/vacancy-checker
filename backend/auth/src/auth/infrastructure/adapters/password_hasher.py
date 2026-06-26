import hashlib
import secrets

from auth.application.ports import PasswordHasher


class PasswordHasherImpl(PasswordHasher):
    _ALGORITHM = "pbkdf2_sha256"
    _DIGEST = "sha256"
    _ITERATIONS = 600_000

    def hash(self, password: str) -> str:
        salt = secrets.token_hex(32)
        dk = hashlib.pbkdf2_hmac(
            self._DIGEST,
            password.encode("utf-8"),
            salt.encode("utf-8"),
            self._ITERATIONS,
        )
        digest = dk.hex()
        return f"{self._ALGORITHM}${self._ITERATIONS}${salt}${digest}"

    def verify(self, password: str, password_hash: str) -> bool:
        algorithm, iterations_str, salt, digest = password_hash.split("$", 3)
        iterations = int(iterations_str)
        dk = hashlib.pbkdf2_hmac(
            algorithm.replace("pbkdf2_", ""),
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
        )
        return secrets.compare_digest(dk.hex(), digest)

    def extract_salt(self, password_hash: str) -> str:
        return password_hash.split("$")[2]
