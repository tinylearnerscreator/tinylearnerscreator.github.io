"""Build the QR code images that videos use to send viewers to the home page.

img/qr/home-qr.png    plain QR, 1000 px, black on white with a quiet zone
img/qr/home-card.png  white rounded card: QR, "Grown-ups: books & printables",
                      "tinylearnerscreator.github.io". Transparent corners.
Run: python3 tools/make_qr.py   (needs: pip install qrcode pillow opencv-python-headless)
"""
import qrcode, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
URL = "https://tinylearnerscreator.github.io/"
F = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
q.add_data(URL); q.make(fit=True)
qr = q.make_image(fill_color="black", back_color="white").convert("RGB").resize((1000, 1000), Image.NEAREST)
qr.save("img/qr/home-qr.png")

W, H, R = 1000, 1290, 70
card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(card)
d.rounded_rectangle([0, 0, W - 1, H - 1], R, fill=(255, 255, 255, 255), outline=(31, 22, 84, 255), width=14)
card.paste(qr.resize((860, 860), Image.NEAREST), (70, 60))
for text, size, y, col in [("Grown-ups: books & printables", 62, 950, (31, 22, 84)),
                           ("tinylearnerscreator.github.io", 54, 1060, (90, 70, 190))]:
    f = ImageFont.truetype(F, size)
    while d.textlength(text, font=f) > W - 80:
        size -= 2; f = ImageFont.truetype(F, size)
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=col)
card.save("img/qr/home-card.png")

# Check both decode to the right address, also at small size.
for p, s in [("img/qr/home-qr.png", 1000), ("img/qr/home-card.png", 1000), ("img/qr/home-card.png", 220)]:
    im = Image.open(p).convert("RGB")
    im = im.resize((s, int(im.height * s / im.width)))
    bg = Image.new("RGB", (im.width + 80, im.height + 80), (120, 60, 200)); bg.paste(im, (40, 40))
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR))
    assert data == URL, (p, s, data)
    print("ok", p, "at", s, "px:", data)
