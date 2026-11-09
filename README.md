# example-repo

Bogus "daily digest" code with a **deliberately brittle contract test** against Wikipedia's daily featured-content feed (`https://en.wikipedia.org/api/rest_v1/feed/featured/YYYY/MM/DD`).

The test always fetches *today's* feed (UTC), but every expectation is pinned to values captured on **2026-11-09**: the featured article's title, description and exact extract length; the top three most-read articles and the top one's exact view count; the picture of the day; section sizes; the exact set of top-level keys; and the exact `Content-Type`, including the feed spec version. It passes on 2026-11-09 and breaks from 2026-11-10 onward, or sooner if Wikipedia edits that day's content.

## Run

```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -m contract -v
```
