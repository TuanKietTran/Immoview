from __future__ import annotations

from django.db import connection
from django.db.models import QuerySet


def _require_postgres() -> None:
    if connection.vendor != "postgresql":
        raise RuntimeError("geo and FTS search require PostgreSQL/PostGIS")


def radius_search(queryset: QuerySet, latitude: float, longitude: float, radius_m: int) -> QuerySet:
    _require_postgres()
    return queryset.extra(
        where=[
            "ST_DWithin(ST_SetSRID(ST_MakePoint(CAST(longitude AS double precision), CAST(latitude AS double precision)), 4326)::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s)"
        ],
        params=[longitude, latitude, radius_m],
    )


def bbox_search(queryset: QuerySet, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> QuerySet:
    _require_postgres()
    return queryset.filter(latitude__gte=min_lat, latitude__lte=max_lat, longitude__gte=min_lon, longitude__lte=max_lon)


def polygon_search(queryset: QuerySet, polygon_wkt: str) -> QuerySet:
    _require_postgres()
    return queryset.extra(
        where=[
            "ST_Contains(ST_GeomFromText(%s, 4326), ST_SetSRID(ST_MakePoint(CAST(longitude AS double precision), CAST(latitude AS double precision)), 4326))"
        ],
        params=[polygon_wkt],
    )


def trigram_search(queryset: QuerySet, term: str, threshold: float = 0.2) -> QuerySet:
    _require_postgres()
    return queryset.extra(
        where=["similarity(unaccent(title), unaccent(%s)) >= %s"],
        params=[term, threshold],
    )


def text_search(queryset: QuerySet, term: str) -> QuerySet:
    _require_postgres()
    return queryset.extra(
        where=[
            "to_tsvector('simple', unaccent(coalesce(title, '') || ' ' || coalesce(description, ''))) @@ plainto_tsquery('simple', unaccent(%s))"
        ],
        params=[term],
    )
