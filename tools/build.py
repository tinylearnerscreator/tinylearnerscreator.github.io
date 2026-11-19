#!/usr/bin/env python3
"""Build links.html from tools/books.json.
Run from the repo root:  python3 tools/build.py
To add a book: add an entry to tools/books.json (and a cover in img/books/), then rebuild.
Formats: paperback, hardcover, kindle, print (printable PDF)."""
import json, html, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((root / "tools" / "books.json").read_text())
e = html.escape
SITE = d["site"]
FORMAT_LABEL = {"paperback": ("Paperback", "Amazon"), "hardcover": ("Hardcover", "Amazon"),
                "kindle": ("Kindle", "Amazon"), "print": ("Printable", "Etsy")}
KIND_LABEL = {"coloring": "Coloring", "mazes": "Mazes", "wordsearch": "Word search",
              "search": "Search and find", "comics": "Comics"}
books = d["books"]
cover = {b["slug"]: b.get("cover") for b in books}

def cover_img(slug, alt="", cls=""):
    return f'<img class="{cls}" src="img/books/{slug}.jpg" width="480" height="623" alt="{e(alt)}" loading="lazy" decoding="async">'

def card(b):
    fm = b["formats"]
    tags = " ".join(["k-" + b["kind"]] + ["t-" + t for t in b["themes"]])
    f_attr = " ".join(fm.keys())
    if b.get("cover"):
        art = cover_img(b["cover"], f'Cover of {b["title"]}', "cv")
    else:
        art = ('<div class="cv cv-chuck" role="img" aria-label="Cover of Agent Chuck: Reply All">'
               '<span class="c1">Agent</span><span class="c2">Chuck</span><span class="c3">Reply All</span>'
               '<span class="c4">Full color comic</span></div>')
    flag = '<span class="flag">New</span>' if b.get("new") else ""
    btns = ""
    for key, v in fm.items():
        label, store = FORMAT_LABEL[key]
        btns += (f'<a class="buy buy-{key}" href="{e(v["url"])}" target="_blank" rel="noopener" '
                 f'aria-label="{e(label)} of {e(b["title"])} on {store}, {e(v["price"])}">'
                 f'<span class="bl">{label}<small>{"PDF on Etsy" if key=="print" else "on "+store}</small></span><span class="bp">{e(v["price"])}</span></a>')
    return (f'<li class="book" data-kind="{b["kind"]}" data-themes="{" ".join(b["themes"])}" data-formats="{f_attr}">'
            f'<div class="art">{art}{flag}</div>'
            f'<h3>{e(b["title"])}</h3>'
            f'<p class="meta">Ages {e(b["ages"])}. {e(b["detail"])}.</p>'
            f'<div class="buys">{btns}</div></li>')

cards = "\n".join(card(b) for b in books)
hero = "".join(f'<li>{cover_img(s, "", "hc")}</li>' for s in d["hero"])
bd = d["bundle"]
bundle_covers = "".join(cover_img(s, "", "bc") for s in bd["covers"])
vids = "".join(
    f'<a class="vid" href="https://youtu.be/{v["id"]}" target="_blank" rel="noopener">'
    f'<img src="https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg" width="480" height="360" alt="" loading="lazy">'
    f'<span class="play" aria-hidden="true"></span><span class="vt">{e(v["title"])}<small>{e(v["note"])}</small></span></a>'
    for v in d["videos"])
kinds_present = [k for k in ["coloring", "mazes", "wordsearch", "search", "comics"] if any(b["kind"] == k for b in books)]
chips = '<button type="button" class="chip" data-filter="all" aria-pressed="true">All books</button>'
if any("christmas" in b["themes"] for b in books):
    chips += '<button type="button" class="chip" data-filter="t:christmas" aria-pressed="false">Christmas</button>'
for k in kinds_present:
    chips += f'<button type="button" class="chip" data-filter="k:{k}" aria-pressed="false">{KIND_LABEL[k]}</button>'

TEMPLATE = (root / "tools" / "template.html").read_text()
out = (TEMPLATE.replace("{{HERO}}", hero).replace("{{CARDS}}", cards).replace("{{CHIPS}}", chips)
       .replace("{{VIDS}}", vids).replace("{{BUNDLE_COVERS}}", bundle_covers)
       .replace("{{BUNDLE_TITLE}}", e(bd["title"])).replace("{{BUNDLE_DETAIL}}", e(bd["detail"]))
       .replace("{{BUNDLE_PRICE}}", e(bd["price"])).replace("{{BUNDLE_URL}}", e(bd["url"]))
       .replace("{{YT}}", SITE["youtube"]).replace("{{TT}}", SITE["tiktok"])
       .replace("{{AMZ}}", SITE["amazon_author"]).replace("{{ETSY}}", SITE["etsy_shop"])
       .replace("{{COUNT}}", str(len(books))))
(root / "links.html").write_text(out)
print("wrote links.html with", len(books), "books")
