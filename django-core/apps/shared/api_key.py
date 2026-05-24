import hashlib
import secrets
import string

_PREFIX = "imv_live_"
_ALPHABET = string.ascii_letters + string.digits
_BODY_LEN = 32


def generate() -> tuple[str, str, str]:
    """
    Returns (raw_key, display_prefix, key_hash).

    raw_key       — shown once to the user, never stored.
    display_prefix — "imv_live_" + last 4 chars; safe to show in the UI.
    key_hash      — SHA-256 hex; stored in the DB.
    """
    body = "".join(secrets.choice(_ALPHABET) for _ in range(_BODY_LEN))
    raw_key = _PREFIX + body
    display_prefix = _PREFIX + body[-4:]
    key_hash = _hash(raw_key)
    return raw_key, display_prefix, key_hash


def _hash(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


def verify(raw_key: str, stored_hash: str) -> bool:
    return secrets.compare_digest(_hash(raw_key), stored_hash)
