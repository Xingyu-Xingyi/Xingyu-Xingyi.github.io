#!/usr/bin/env python3
# 用途：把四个页面里 <!--HEADER--> 到 <!--/HEADER--> 之间换成同一份页头，顺便保证每页都引了 theme.css

import pathlib
import re

SITE = pathlib.Path(__file__).parent

# 页面 → (页面名, 标题下面的小字, 导航里高亮的那一项)
PAGES = {
    "index.html": ("林柚咲", "计算机 · 大一 · 伦敦", "./"),
    "works.html": ("做过的", "按时间倒着来", "./works.html"),
    "code.html": ("代码片段", "左边挑一条，右边看", "./code.html"),
    "notes.html": ("笔记", "讲到哪写到哪", "./notes.html"),
    "diary.html": ("日记", "写干了什么，也写心里那层", "./diary.html"),
}

NAV = [
    ("做过的", "./works.html"),
    ("代码片段", "./code.html"),
    ("笔记", "./notes.html"),
    ("日记", "./diary.html"),
]

HEADER = """  <!--HEADER-->
  <header class="site-header">
    <a class="brand" href="./">{brand}<span class="dot">·</span><span class="brand-sub">{sub}</span></a>
    <nav class="site-nav">
{links}
    </nav>
  </header>
  <!--/HEADER-->"""


def nav_html(current):
    out = []
    for label, href in NAV:
        mark = ' aria-current="page"' if href == current else ""
        out.append(f'      <a href="{href}"{mark}>{label}</a>')
    return "\n".join(out)


def build(name, brand, sub, current):
    path = SITE / name
    html = path.read_text(encoding="utf-8")

    header = HEADER.format(brand=brand, sub=sub, links=nav_html(current))
    new, n = re.subn(
        r"  <!--HEADER-->.*?<!--/HEADER-->",
        header,
        html,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"{name}: 占位块数量不对（{n}）")

    if 'href="theme.css"' not in new:
        new = new.replace(
            "</title>",
            '</title>\n<link rel="stylesheet" href="theme.css">',
            1,
        )
    if new != html:
        path.write_text(new, encoding="utf-8")
        print(f"{name}: 更新")
    else:
        print(f"{name}: 没变化")


for name, (brand, sub, current) in PAGES.items():
    build(name, brand, sub, current)
