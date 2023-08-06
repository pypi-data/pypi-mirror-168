from feedparser import parse as parse_feed
from typing import List

from info_ut.feed import Feed


def get_feed(url: str, etag: str = None, modified: str = None) -> Feed:
    feed = parse_feed(url, etag=etag, modified=modified)
    return Feed.from_feed(feed)


def get_pengumuman(etag: str = None, modified: str = None) -> Feed:
    url = "https://www.ut.ac.id/pengumuman.xml"
    return get_feed(url, etag, modified)


def get_berita(etag: str = None, modified: str = None) -> Feed:
    url = "https://www.ut.ac.id/berita.xml"
    return get_feed(url, etag, modified)
