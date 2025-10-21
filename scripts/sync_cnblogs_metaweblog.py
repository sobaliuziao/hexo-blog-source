import os
import xmlrpc.client
import frontmatter
from pathlib import Path
from bs4 import BeautifulSoup

# ─── 配置 ─────────────────────────────
USER = os.getenv("CNBLOGS_USER")
TOKEN = os.getenv("CNBLOGS_TOKEN")
POST_DIR = Path("source/_posts")
POST_DIR.mkdir(parents=True, exist_ok=True)

if not USER or not TOKEN:
    raise ValueError("❌ Missing CNBLOGS_USER or CNBLOGS_TOKEN env variables")

# 博客园 blogid
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

    # ─── 处理 HTML 内容 ─────────────────
    soup = BeautifulSoup(html_content, "html.parser")

    # 1️⃣ 保留代码块，转换成 ```cpp ```
    for pre in soup.find_all("pre"):
        code_text = pre.get_text()
        pre.string = f"```cpp\n{code_text}\n```"

    # 2️⃣ 移除 script/style
    for tag in soup(["script", "style"]):
        tag.decompose()

    # 3️⃣ 转 Markdown（不转换 <pre> 内的内容）
    markdown_text = ""
    for child in soup.children:
        # 如果是 <pre> 则直接取 text
        if child.name == "pre":
            markdown_text += child.get_text() + "\n\n"
        else:
            # 其他节点转成文本
            markdown_text += child.get_text(separator="\n") + "\n\n"

    # ─── 处理日期 ─────────────────
    date_obj = post.get("dateCreated")
    if isinstance(date_obj, xmlrpc.client.DateTime):
        date_str = date_obj.value  # "YYYYMMDDTHH:MM:SS"
        date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {date_str[9:]}"
    else:
        date_str = str(date_obj)

    # ─── 分类与标签 ─────────────────
    categories = post.get("categories", [])
    tags = post.get("mt_keywords", "").split(",") if post.get("mt_keywords") else []

    # ─── 文件名处理 ─────────────────
    safe_title = "".join(c if c.isalnum() or c in "-_ " else "-" for c in title).strip()
    filename = POST_DIR / f"{safe_title}.md"

    # 跳过已存在文章
    if filename.exists():
        print(f"⏩ Skipping existing post: {title}")
        continue

    # ─── 构建 frontmatter ─────────────────
    fm_post = frontmatter.Post(markdown_text)
    fm_post.metadata = {
        "title": title,
        "date": date_str,
        "categories": categories or ["Cnblogs"],
        "tags": tags,
    }

    # ─── 写入文件 ─────────────────
    with open(filename, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(fm_post))

    print(f"✅ Synced: {title}")

print("🎉 All posts synced successfully!")
