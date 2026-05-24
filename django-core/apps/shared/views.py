import base64
import logging
from django.http import JsonResponse
from decouple import config

logger = logging.getLogger(__name__)


def jwks(request):
    """
    GET /.well-known/jwks.json
    Returns the RSA public key as a JWK set for RS256 JWT verification.
    Lambdas and external services fetch this once at cold-start and cache.
    Returns 404 when running in HS256 mode (dev without RSA keys configured).
    """
    pub_key_b64 = config("JWT_PUBLIC_KEY_B64", default="")
    if not pub_key_b64:
        return JsonResponse(
            {"detail": "JWKS not available — server is in HS256 mode"},
            status=404,
        )

    try:
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

        pub_pem = base64.b64decode(pub_key_b64)
        public_key = load_pem_public_key(pub_pem)

        if not isinstance(public_key, RSAPublicKey):
            return JsonResponse({"detail": "Only RSA keys are supported"}, status=500)

        nums = public_key.public_numbers()

        def _int_to_base64url(n: int) -> str:
            length = (n.bit_length() + 7) // 8
            return base64.urlsafe_b64encode(n.to_bytes(length, "big")).rstrip(b"=").decode()

        jwk = {
            "kty": "RSA",
            "use": "sig",
            "alg": "RS256",
            "n": _int_to_base64url(nums.n),
            "e": _int_to_base64url(nums.e),
        }
        return JsonResponse({"keys": [jwk]}, content_type="application/json")

    except Exception:
        logger.exception("JWKS endpoint failed")
        return JsonResponse({"detail": "Key configuration error"}, status=500)
