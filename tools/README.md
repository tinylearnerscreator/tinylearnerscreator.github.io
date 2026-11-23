# Links page tools

index.html and links.html are generated (the same page). Do not edit either by hand. The footer keeps the Tiny Learners Media app text and Privacy and Terms links, which Google and TikTok app reviews need on the home page.

To add or change a book:
1. Put the front cover in img/books/<slug>.jpg (480 px wide, JPEG).
2. Add or edit the entry in tools/books.json. Formats: paperback, hardcover, kindle, print (printable PDF).
3. Run: python3 tools/build.py
4. Commit links.html, tools/books.json and the cover.

Agent Chuck has no cover file yet. Set "cover" to its slug once img/books/agent-chuck.jpg exists.

QR code for videos:
- img/qr/home-qr.png and img/qr/home-card.png point to https://tinylearnerscreator.github.io/. Rebuild with python3 tools/make_qr.py (it checks both decode).
- tools/add_qr.sh IN.mp4 OUT.mp4 [SECONDS] puts the card on the last seconds of a video (default 4 s). Wide videos get it bottom right, tall videos on the left above TikTok's bottom 22 percent.
