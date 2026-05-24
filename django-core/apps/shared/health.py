import time
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def liveness(request):
    return JsonResponse({"status": "ok"})


def readiness(request):
    checks = {}
    ok = True

    # PostgreSQL
    try:
        t0 = time.monotonic()
        from django.db import connection
        connection.ensure_connection()
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
        checks["postgresql"] = {"status": "healthy", "latency_ms": round((time.monotonic() - t0) * 1000, 1)}
    except Exception as exc:
        checks["postgresql"] = {"status": "unhealthy", "error": str(exc)}
        ok = False

    # Redis
    try:
        t0 = time.monotonic()
        from django.core.cache import cache
        cache.set("_health", "1", timeout=5)
        assert cache.get("_health") == "1"
        checks["redis"] = {"status": "healthy", "latency_ms": round((time.monotonic() - t0) * 1000, 1)}
    except Exception as exc:
        checks["redis"] = {"status": "unhealthy", "error": str(exc)}
        ok = False

    status_code = 200 if ok else 503
    return JsonResponse({"status": "healthy" if ok else "unhealthy", "checks": checks}, status=status_code)


def services(request):
    """
    Control-plane: aggregates health of every dependent service.
    Critical: postgresql, redis — failure → 503.
    Degraded: Lambda, SQS, DynamoDB — failure → 207.
    """
    result: dict = {}
    critical_ok = True
    any_degraded = False

    # PostgreSQL
    try:
        t0 = time.monotonic()
        from django.db import connection
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
        result["postgresql"] = {"status": "healthy", "latency_ms": round((time.monotonic() - t0) * 1000, 1)}
    except Exception as exc:
        result["postgresql"] = {"status": "unhealthy", "error": str(exc)}
        critical_ok = False

    # Redis
    try:
        t0 = time.monotonic()
        from django.core.cache import cache
        cache.set("_health_services", "1", timeout=5)
        assert cache.get("_health_services") == "1"
        result["redis"] = {"status": "healthy", "latency_ms": round((time.monotonic() - t0) * 1000, 1)}
    except Exception as exc:
        result["redis"] = {"status": "unhealthy", "error": str(exc)}
        critical_ok = False

    # AWS / LocalStack services
    try:
        from apps.shared.aws import sqs_client, dynamodb_resource
        from decouple import config

        # SQS queue
        try:
            queue_url = config("SQS_LEAD_SCORING_URL", default="")
            if queue_url:
                sqs_client().get_queue_attributes(QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"])
                result["sqs_lead_scoring"] = {"status": "healthy"}
            else:
                result["sqs_lead_scoring"] = {"status": "unconfigured"}
        except Exception as exc:
            result["sqs_lead_scoring"] = {"status": "unhealthy", "error": str(exc)}
            any_degraded = True

        # DynamoDB table
        try:
            table = dynamodb_resource().Table(config("DYNAMODB_LEAD_SCORES_TABLE", default="lead-scores"))
            table.load()
            result["dynamodb_lead_scores"] = {"status": "healthy", "item_count": table.item_count}
        except Exception as exc:
            result["dynamodb_lead_scores"] = {"status": "unhealthy", "error": str(exc)}
            any_degraded = True

        # Lambda functions
        _check_lambdas(result)
        if any(v.get("status") == "unhealthy" for k, v in result.items() if k.startswith("lambda_")):
            any_degraded = True

    except Exception as exc:
        result["aws"] = {"status": "unhealthy", "error": str(exc)}
        any_degraded = True

    if not critical_ok:
        overall = "unhealthy"
        status_code = 503
    elif any_degraded:
        overall = "degraded"
        status_code = 207
    else:
        overall = "healthy"
        status_code = 200

    return JsonResponse(
        {
            "status": overall,
            "timestamp": _now_iso(),
            "services": result,
        },
        status=status_code,
    )


def _check_lambdas(result: dict) -> None:
    import boto3
    from decouple import config
    import botocore

    endpoint = config("AWS_ENDPOINT_URL", default="")
    kwargs = {
        "region_name": config("AWS_DEFAULT_REGION", default="eu-central-1"),
        "aws_access_key_id": config("AWS_ACCESS_KEY_ID", default=""),
        "aws_secret_access_key": config("AWS_SECRET_ACCESS_KEY", default=""),
    }
    if endpoint:
        kwargs["endpoint_url"] = endpoint

    client = boto3.client("lambda", **kwargs)

    for name in ("lead-scoring", "image-pipeline", "notifications"):
        key = f"lambda_{name.replace('-', '_')}"
        try:
            resp = client.get_function(FunctionName=name)
            state = resp["Configuration"].get("State", "Unknown")
            result[key] = {"status": "healthy" if state == "Active" else "degraded", "state": state}
        except botocore.exceptions.ClientError as exc:
            code = exc.response["Error"]["Code"]
            if code == "ResourceNotFoundException":
                result[key] = {"status": "not_deployed"}
            else:
                result[key] = {"status": "unhealthy", "error": str(exc)}
        except Exception as exc:
            result[key] = {"status": "unhealthy", "error": str(exc)}


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
