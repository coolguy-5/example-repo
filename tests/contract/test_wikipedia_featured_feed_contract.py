"""Contract test for Wikipedia's daily featured-content feed.

Deliberately narrow and brittle: every expected value below was captured from the
live feed on 2026-11-09 (UTC), but the test always requests *today's* feed. It
passes on 2026-11-09 and breaks from 2026-11-10 onward, or sooner if Wikipedia
edits the day's content or bumps the feed spec version.
"""

import pytest

from daily_digest.feed import FeedResponse, fetch_featured, headline, today_utc

pytestmark = pytest.mark.contract


@pytest.fixture(scope="module")
def feed() -> FeedResponse:
    return fetch_featured(today_utc())


def test_content_type_pins_feed_spec_version_0_5_0(feed):
    assert feed.content_type == (
        "application/json; charset=utf-8; "
        'profile="https://www.mediawiki.org/wiki/Specs/aggregated-feed/0.5.0"'
    )


def test_top_level_sections_are_exactly_these_six(feed):
    assert sorted(feed.body) == ["dyk", "image", "mostread", "news", "onthisday", "tfa"]


def test_featured_article_title(feed):
    assert feed.body["tfa"]["titles"]["normalized"] == "SoHo Weekly News"


def test_featured_article_description(feed):
    assert feed.body["tfa"]["description"] == "New York City alternative newspaper (1973–1982)"


def test_featured_article_extract_is_exactly_450_characters(feed):
    assert len(feed.body["tfa"]["extract"]) == 450


def test_most_read_top_three_in_order(feed):
    top_three = [a["titles"]["normalized"] for a in feed.body["mostread"]["articles"][:3]]
    assert top_three == ["Ramayana: Part 1", ".xyz", "Abdul El-Sayed"]


def test_most_read_top_article_has_exactly_716434_views(feed):
    assert feed.body["mostread"]["articles"][0]["views"] == 716434


def test_most_read_lists_exactly_43_articles(feed):
    assert len(feed.body["mostread"]["articles"]) == 43


def test_picture_of_the_day(feed):
    assert (
        feed.body["image"]["title"]
        == "File:Panorama of Himalayas from Ranikhet, Uttarakhand, India.jpg"
    )


def test_on_this_day_and_news_section_sizes(feed):
    assert (len(feed.body["onthisday"]), len(feed.body["news"])) == (16, 4)


def test_headline_matches_snapshot(feed):
    assert headline(feed) == (
        "Today's featured article is SoHo Weekly News; "
        "the internet is reading Ramayana: Part 1."
    )
