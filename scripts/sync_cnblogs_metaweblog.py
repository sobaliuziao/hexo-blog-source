import os
import xmlrpc.client
import frontmatter
from markdownify import markdownify as md

USER = os.getenv("Scarab")
TOKEN = os.getenv("79A65BB1FC15A4BCE6B55990EF8ED4DCCD7F36C549E56DAC7EDE09C40C9DD785")

if not USER or not TOKEN:
    raise ValueError("❌ Missing CNBLOGS_USER or CNBLOGS_TOKEN env variables")

BLOG_ID = f"https://www.cnblogs.com/Scarab/"
server = xmlrpc.client.ServerProxy(
    f"https://rpc.cnblogs.com/metaweblog/Scarab",
    allow_none=True
)

print("🚀 Syncing from Cnblogs...")

# ✅ blogid, username, password, numberOfPosts
posts = server.metaWeblog.getRecentPosts(BLOG_ID, USER, TOKEN, 50)

os.makedirs("source/_posts", exist_ok=True)

for post in posts:
    title = post["title"]
    html_content = post["description"]
    markdown = md(html_content)

    fm = {
        "title": title,
        "date": post["dateCreated"].isoformat(),
        "categories": post.get("categories", []),
        "tags": post.get("mt_keywords", "").split(",") if post.get("mt_keywords") else [],
    }

    filename = f"source/_posts/{title.replace(' ', '-')}.md"
    post_data = frontmatter.Post(markdown, **fm)

    with open(filename, "w", encoding="utf-8") as f:
        frontmatter.dump(post_data, f)

    print(f"✅ Synced: {title}")

print("🎉 All posts synced!")
