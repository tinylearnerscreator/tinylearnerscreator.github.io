# Links page tools

index.html and links.html are generated (the same page). Do not edit either by hand. The footer keeps the Tiny Learners Media app text and Privacy and Terms links, which Google and TikTok app reviews need on the home page.

To add or change a book:
1. Put the front cover in img/books/<slug>.jpg (480 px wide, JPEG).
2. Add or edit the entry in tools/books.json. Formats: paperback, hardcover, kindle, print (printable PDF).
3. Run: python3 tools/build.py
4. Commit links.html, tools/books.json and the cover.

Agent Chuck has no cover file yet. Set "cover" to its slug once img/books/agent-chuck.jpg exists.
