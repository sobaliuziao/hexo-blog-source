import os
import re
import requests
import frontmatter
from datetime import datetime
from xmlrpc.client import ServerProxy
from markdownify import markdownify as md
from pathlib import Path
from bs4 import BeautifulSoup

API_URL = f"https://rpc.cnblogs.com/metaweblog/{os.getenv('Scarab')}"
USER = os.getenv("Scarab")
TOKEN = os.getenv("79A65BB1FC15A4BCE6B55990EF8ED4DCCD7F36C549E56DAC7EDE09C40C9DD785")

POST_DIR = Path("source/_posts")
POST_DIR.mkdir(parents=True, exist_ok=True)

def slugify(title):
    return re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", title).strip("-")

server = ServerProxy(API_URL)
posts = server.metaWeblog.getRecentPosts(USER, USER, TOKEN, 50)  # 最近50篇

for post in posts:
    title = post["title"]
    date = datetime.strptime(post["dateCreated"].value.isoformat(), "%Y-%m-%dT%H:%M:%S")
    categories = post.get("categories", [])
    tags = post.get("mt_keywords", "").split(",") if post.get("mt_keywords") else []

    filename = f"{slugify(title)}.md"
    path = POST_DIR / filename
    if path.exists():
        continue

    html = post["description"]

    # 用 BeautifulSoup 清理 cnblogs 的样式
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    content_html = str(soup)
    md_text = md(content_html)

    post_md = frontmatter.Post(md_text)
    post_md.metadata = {
        "title": title,
        "date": date.strftime("%Y-%m-%d %H:%M:%S"),
        "categories": categories or ["Cnblogs"],
        "tags": tags,
    }

    with open(path, "w", encoding="utf-8") as f:
        frontmatter.dump(post_md, f)

    print(f"✅ Saved {filename}")
