import hashlib
import secrets


def generate_token_hash() -> tuple[str, str]:
    raw = secrets.token_hex(64)
    hashed = hash_token(raw)
    return raw, hashed


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
