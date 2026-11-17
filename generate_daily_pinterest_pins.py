import os
import glob
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"C:\Users\prime\Desktop\Pinterest_Pins"
REPO_PIN_DIR = r"C:\Users\prime\Desktop\2026\kidspeechai_repo\pinterest_pins"
FEAT_DIR = r"C:\Users\prime\Desktop\2026\kidspeechai_repo\images\features"

def load_font(size, bold=True):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def render_pins(pins, clear_output=True):
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(REPO_PIN_DIR, exist_ok=True)
    if clear_output:
        for old_png in glob.glob(os.path.join(OUT_DIR, "*.png")):
            try:
                os.remove(old_png)
            except OSError:
                pass

    for p in pins:
        W, H = 1000, 1500
        img = Image.new("RGB", (W, H), p["bg_top"])
        draw = ImageDraw.Draw(img)

        for y in range(H):
            t = y / float(H)
            r = int(p["bg_top"][0] * (1 - t) + p["bg_bottom"][0] * t)
            g = int(p["bg_top"][1] * (1 - t) + p["bg_bottom"][1] * t)
            b = int(p["bg_top"][2] * (1 - t) + p["bg_bottom"][2] * t)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        f_badge = load_font(26, bold=True)
        bbox = draw.textbbox((0, 0), p["badge"], font=f_badge)
        bw = bbox[2] - bbox[0] + 56
        bh = 58
        bx = (W - bw) // 2
        by = 48
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=29, fill=p["badge_bg"])
        draw.text((bx + 28, by + 13), p["badge"], font=f_badge, fill=p["badge_fg"])

        f_title = load_font(60, bold=True)
        title_lines = wrap_text(draw, p["title"], f_title, 880)
        ty = 132
        for line in title_lines:
            lb = draw.textbbox((0, 0), line, font=f_title)
            lw = lb[2] - lb[0]
            draw.text(((W - lw) // 2, ty), line, font=f_title, fill=(255, 255, 255))
            ty += 72

        f_sub = load_font(31, bold=True)
        sub_lines = wrap_text(draw, p["subtitle"], f_sub, 880)
        ty += 6
        for line in sub_lines:
            lb = draw.textbbox((0, 0), line, font=f_sub)
            lw = lb[2] - lb[0]
            draw.text(((W - lw) // 2, ty), line, font=f_sub, fill=(255, 232, 168))
            ty += 42

        card_top = ty + 22
        card_bottom = 860
        draw.rounded_rectangle([60, card_top, W - 60, card_bottom], radius=32, fill=(255, 252, 247))

        f_bullet = load_font(29, bold=True)
        by_cur = card_top + 30
        step_h = (card_bottom - card_top - 44) // len(p["bullets"])
        for b_text in p["bullets"]:
            draw.rounded_rectangle([92, by_cur + 2, 134, by_cur + 44], radius=12, fill=(67, 56, 202))
            draw.line([(102, by_cur + 24), (110, by_cur + 33), (125, by_cur + 14)], fill=(255, 255, 255), width=5)
            draw.text((152, by_cur + 5), b_text, font=f_bullet, fill=(30, 36, 59))
            by_cur += step_h

        feat_path = p.get("feature_img", os.path.join(FEAT_DIR, "popup-images.jpg"))
        if not os.path.isabs(feat_path):
            feat_path = os.path.join(FEAT_DIR, feat_path)
        if os.path.exists(feat_path):
            feat = Image.open(feat_path).convert("RGB")
            target_w, target_h = 880, 440
            feat_ratio = feat.width / feat.height
            if feat_ratio > (target_w / target_h):
                new_h = target_h
                new_w = int(new_h * feat_ratio)
            else:
                new_w = target_w
                new_h = int(new_w / feat_ratio)
            feat = feat.resize((new_w, new_h), Image.Resampling.LANCZOS)
            left = (new_w - target_w) // 2
            top = (new_h - target_h) // 2
            feat = feat.crop((left, top, left + target_w, top + target_h))

            mask = Image.new("L", (target_w, target_h), 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.rounded_rectangle([0, 0, target_w, target_h], radius=28, fill=255)
            img.paste(feat, (60, 885), mask)

        draw.rounded_rectangle([60, 1355, W - 60, 1455], radius=50, fill=(255, 209, 102))
        f_cta = load_font(31, bold=True)
        cb = draw.textbbox((0, 0), p["cta"], font=f_cta)
        cw = cb[2] - cb[0]
        draw.text(((W - cw) // 2, 1386), p["cta"], font=f_cta, fill=(30, 36, 59))

        out_path = os.path.join(OUT_DIR, p["filename"])
        repo_path = os.path.join(REPO_PIN_DIR, p["filename"])
        img.save(out_path, "PNG", optimize=True)
        img.save(repo_path, "PNG", optimize=True)
        print("Saved Pin:", out_path)
