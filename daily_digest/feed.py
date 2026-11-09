"""Bogus daily digest built on Wikipedia's featured-content feed."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone

import requests

FEED_URL = "https://en.wikipedia.org/api/rest_v1/feed/featured/{day:%Y/%m/%d}"
# Wikimedia asks API clients for an identifying User-Agent.
USER_AGENT = "brittle-contract-demo/0.1 (https://github.com/coolguy-5/example-repo)"


@dataclass(frozen=True)
class FeedResponse:
    content_type: str
    body: dict


def today_utc() -> date:
    return datetime.now(timezone.utc).date()


def fetch_featured(day: date, timeout: float = 10.0) -> FeedResponse:
    response = requests.get(
        FEED_URL.format(day=day),
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    return FeedResponse(
        content_type=response.headers["Content-Type"],
        body=response.json(),
    )


def headline(feed: FeedResponse) -> str:
    featured = feed.body["tfa"]["titles"]["normalized"]
    most_read = feed.body["mostread"]["articles"][0]["titles"]["normalized"]
    return f"Today's featured article is {featured}; the internet is reading {most_read}."
