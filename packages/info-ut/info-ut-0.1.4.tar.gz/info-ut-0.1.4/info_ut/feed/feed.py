import attr
import time
from datetime import datetime
from feedparser import FeedParserDict
from typing import Iterator, List, Optional

from . import FeedItem


@attr.dataclass
class Feed:
    title: str
    link: str
    description: str
    etag: str
    updated: datetime
    items: List[FeedItem] = attr.field(factory=list)

    def __attrs_post_init__(self) -> None:
        if isinstance(self.updated, time.struct_time):
            self.updated = datetime.fromtimestamp(time.mktime(self.updated))
        new_items: List[FeedItem] = list()
        for item in self.items:
            new_items.append(FeedItem.from_dict(item))
        self.items = new_items

    def __iter__(self) -> Iterator[FeedItem]:
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    @classmethod
    def from_feed(cls, feed: FeedParserDict) -> "Feed":
        return cls(
            title=feed.feed.title,
            link=feed.feed.link,
            description=feed.feed.description,
            etag=feed.etag,
            updated=feed.updated,
            items=feed.entries,
        )
