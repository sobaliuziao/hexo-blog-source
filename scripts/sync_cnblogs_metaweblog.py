import os
import xmlrpc.client
import frontmatter
from markdownify import markdownify as md
from pathlib import Path
from bs4 import BeautifulSoup

# ─── 配置 ─────────────────────────────
USER = os.getenv("CNBLOGS_USER")
TOKEN = os.getenv("CNBLOGS_TOKEN")
POST_DIR = Path("source/_posts")
POST_DIR.mkdir(parents=True, exist_ok=True)

if not USER or not TOKEN:
    raise ValueError("❌ Missing CNBLOGS_USER or CNBLOGS_TOKEN env variables")

# 博客园 blogid 格式
BLOG_ID = f"https://www.cnblogs.com/{USER}/"

# 创建 ServerProxy
server = xmlrpc.client.ServerProxy(
    f"https://rpc.cnblogs.com/metaweblog/{USER}",
    allow_none=True
)

print("🚀 Syncing from Cnblogs...")

# ─── 获取最近50篇文章 ─────────────────
posts = server.metaWeblog.getRecentPosts(BLOG_ID, USER, TOKEN, 50)

for post in posts:
    title = post.get("title", "untitled")
    html_content = post.get("description", "")

    # 清理 HTML
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    clean_html = str(soup)

    # 转 Markdown
    markdown_text = md(clean_html)

    # 处理日期
    date_obj = post.get("dateCreated")
    if isinstance(date_obj, xmlrpc.client.DateTime):
        date_str = date_obj.value  # "YYYYMMDDTHH:MM:SS"
        date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {date_str[9:]}"
    else:
        date_str = str(date_obj)

    # 分类与标签
    categories = post.get("categories", [])
    tags = post.get("mt_keywords", "").split(",") if post.get("mt_keywords") else []

    # 生成安全文件名
    safe_title = "".join(c if c.isalnum() or c in "-_ " else "-" for c in title).strip()
    filename = POST_DIR / f"{safe_title}.md"

    # 跳过已存在文章
    if filename.exists():
        print(f"⏩ Skipping existing post: {title}")
        continue

    # 构建 frontmatter
    fm_post = frontmatter.Post(markdown_text)
    fm_post.metadata = {
        "title": title,
        "date": date_str,
        "categories": categories or ["Cnblogs"],
        "tags": tags,
    }

    # 写入文件（修复 write bytes 报错）
    with open(filename, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(fm_post))

    print(f"✅ Synced: {title}")

print("🎉 All posts synced successfully!")
