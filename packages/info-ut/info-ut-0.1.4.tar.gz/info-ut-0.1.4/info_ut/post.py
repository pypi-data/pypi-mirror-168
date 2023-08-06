import attr
import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Optional


BASE_URL = "https://www.ut.ac.id"


@attr.dataclass(slots=True)
class Post:
    title: str
    link: str
    content: str
    cover_img: Optional[str] = None
    imgs: List[str] = attr.field(factory=list)
    tags: List[str] = attr.field(factory=list)

    @classmethod
    def from_link(cls, link: str):
        res = requests.get(link)
        assert res.ok and res.text
        soup = BeautifulSoup(res.text, "html.parser")
        post_title: str = soup.find("h1", class_="page_title").get_text()
        main_block: Tag = soup.find("div", id="block-system-main")
        try:
            cover_section: Tag = main_block.find(
                "div", class_="field-name-field-media-pengumuman"
            )
            cover_content: Tag = cover_section.find("div", class_="content")
            post_cover_img: Optional[str] = cover_content.find("img")["href"]
        except Exception:
            post_cover_img = None
        post_section: Tag = main_block.find("section", class_="post-content")
        post_content: Tag = post_section.find("div", class_="field-name-body")
        imgs: List[str] = list()
        for img in post_content.find_all("img"):
            img_url: str = img.attrs.get("src", "")
            if not img_url:
                continue
            if img_url.startswith("/"):
                imgs.append(BASE_URL + img_url)
            else:
                imgs.append(img_url)
        tags_content: Tag = main_block.find("div", class_="field-name-field-tags")
        tags: List[str] = list()
        for tag in tags_content.find_all("div", "field-item"):
            a_tag = tag.find("a")
            if a_tag:
                tags.append(a_tag.get_text())
        return cls(
            title=post_title,
            link=link,
            content=str(post_content),
            cover_img=post_cover_img,
            imgs=imgs,
            tags=tags,
        )
