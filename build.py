#!/usr/bin/env python3
"""
REGINA site generator.
Builds index.html + one page per product category from shared header/footer
templates + external CSS/JS, so every page stays in sync automatically.
Run: python3 build.py
"""
import re

ROOT = "/home/claude/regina-site"

HEADER_TPL = open(f"{ROOT}/_header_template.html", encoding="utf-8").read()
CONTACT_FOOTER = open(f"{ROOT}/_contact_footer.html", encoding="utf-8").read()
MARQUEE = open(f"{ROOT}/_marquee.html", encoding="utf-8").read()

CATEGORIES = ["caps", "hats", "tshirts", "coverall", "graduation"]
NAV_SLUGS = CATEGORIES + ["customize"]

def header_for(active_slug):
    html = HEADER_TPL
    for slug in NAV_SLUGS:
        cls = "active" if slug == active_slug else ""
        html = html.replace(f"{{{{ACTIVE_{slug}}}}}", cls)
    return html

DOC_HEAD = """<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="dark" data-lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/logos/regina-red.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
"""

DOC_TAIL = """
<script src="assets/js/main.js"></script>
</body>
</html>
"""

def page(title, desc, active_slug, body_sections):
    return (
        DOC_HEAD.format(title=title, desc=desc)
        + header_for(active_slug)
        + body_sections
        + CONTACT_FOOTER
        + DOC_TAIL
    )

def write(name, content):
    with open(f"{ROOT}/{name}", "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, len(content), "chars")

# ------------------------------------------------------------------
# Import the existing hero + marquee + products + mockup + about
# sections straight out of the current index.html body so the
# homepage keeps everything it already has.
# ------------------------------------------------------------------
current_index = open(f"{ROOT}/index.html", encoding="utf-8").read()
home_start = current_index.index('<!-- ===================== HERO ===================== -->')
home_end = current_index.index('<!-- ===================== CONTACT ===================== -->')
HOME_BODY = current_index[home_start:home_end]

write("index.html", page(
    "REGINA — Corporate Caps, Uniforms & Branded Workwear · Since 1983",
    "REGINA — Alexandria-based manufacturer of corporate caps, hats, uniforms, coveralls and graduation gear. Since 1983.",
    active_slug=None,
    body_sections=HOME_BODY,
))

print("Base index.html rebuilt from existing sections.")

# ------------------------------------------------------------------
# Category pages
# ------------------------------------------------------------------

PLACEHOLDER_ICON = """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M8 34 C8 20 16 12 24 12 C32 12 40 20 40 34" stroke="currentColor" stroke-width="2"/>
  <path d="M8 34 C14 38 34 38 40 34" stroke="currentColor" stroke-width="2"/>
  <circle cx="24" cy="24" r="4" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 3"/>
</svg>"""

def collection_note():
    return """
    <div class="collection-note">
      <span class="dot"></span>
      <span>
        <span class="en">This collection is being stocked — new items are added regularly. Get in touch for current availability and bulk pricing.</span>
        <span class="ar">الكوليكشن ده لسه بيتزود بمنتجات جديدة أول بأول — كلمنا دلوقتي ونبعتلك على طول المتاح حاليًا والأسعار بالكمية.</span>
      </span>
    </div>"""

def collection_grid(n=8):
    cards = []
    for i in range(1, n + 1):
        cards.append(f"""
      <!-- PRODUCT CARD {i:02d} — duplicate this block for each new item, swap the image + text -->
      <div class="collection-card">
        <div class="cc-img">{PLACEHOLDER_ICON}</div>
        <div>
          <h4><span class="en">Product Name</span><span class="ar">اسم المنتج</span></h4>
          <p class="cc-spec"><span class="en">Add spec / colorway / MOQ</span><span class="ar">أضف المقاس / اللون / أقل كمية</span></p>
        </div>
        <span class="cc-cta"><span class="en">Coming Soon</span><span class="ar">قريبًا جدًا</span></span>
      </div>""")
    return f'\n    <div class="collection-grid reveal">{"".join(cards)}\n    </div>'

def cta_band():
    return """
    <div class="cta-band reveal">
      <h3><span class="en">Want this branded for your company?</span><span class="ar">متخيل الكوليكشن ده وعليه شعار شركتك؟</span></h3>
      <a href="index.html#contact" class="btn btn-ghost">
        <span class="en">Get Your Quote</span><span class="ar">اطلب عرض سعرك</span>
      </a>
    </div>"""

def cat_hero(slug, tag_en, tag_ar, title_en, title_ar, desc_en, desc_ar, image=None):
    if image:
        media = f'<img src="assets/banners/{image}" alt="{title_en}"><div class="hero-overlay"></div>'
        extra_class = ""
    else:
        media = '<img class="cat-hero-mark" src="assets/logos/regina-white.svg" alt=""><div class="hero-overlay"></div>'
        extra_class = " cat-hero-noimg"
    return f"""
<section class="cat-hero-section">
  <div class="wrap">
    <div class="breadcrumb reveal">
      <a href="index.html"><span class="en">Home</span><span class="ar">الرئيسية</span></a>
      <span class="sep">/</span>
      <span class="current"><span class="en">{title_en}</span><span class="ar">{title_ar}</span></span>
    </div>
    <div class="cat-hero{extra_class} reveal" style="margin-top:16px;">
      {media}
      <div class="cat-hero-content">
        <span class="pc-tag"><span class="en">{tag_en}</span><span class="ar">{tag_ar}</span></span>
        <h1><span class="en">{title_en}</span><span class="ar">{title_ar}</span></h1>
        <p><span class="en">{desc_en}</span><span class="ar">{desc_ar}</span></p>
      </div>
    </div>
  </div>
</section>
"""

def cat_body(slug, **kw):
    return (
        cat_hero(slug, **{k: kw[k] for k in ["tag_en","tag_ar","title_en","title_ar","desc_en","desc_ar","image"]})
        + MARQUEE
        + '\n<section class="section-pad" style="padding-top:56px;">\n  <div class="wrap">'
        + collection_note()
        + collection_grid(8)
        + cta_band()
        + '\n  </div>\n</section>\n'
    )

CATEGORY_DATA = {
  "caps": dict(
    tag_en="Headwear", tag_ar="مقتنيات الرأس",
    title_en="Caps", title_ar="الكابات",
    desc_en="Your logo, embroidered clean, on every cap you hand out. Structured 6-panel, snapback, and low-profile caps — sized, colored, and embroidered to your brand guidelines.",
    desc_ar="شعارك مطرز نضيف على كل كاب، عشان أي حد يشوفه يعرف إنه قدام فريق محترم. كابات 6-panel وسناب باك ولو-بروفايل — بالمقاس واللون والتطريز اللي يمثّل هوية شركتك بالظبط.",
    image=None,
    page_title="Caps — REGINA Corporate Headwear",
    page_desc="Custom embroidered corporate caps from REGINA — structured, snapback, and low-profile styles, branded to your company.",
  ),
  "hats": dict(
    tag_en="Headwear", tag_ar="مقتنيات الرأس",
    title_en="Hats", title_ar="البرانيط",
    desc_en="Outdoor teams need hats that survive the shift, not just the photo. Bucket, safari, and wide-brim sun hats for field teams, events, and seasonal campaigns.",
    desc_ar="الفرق اللي شغالة تحت الشمس طول اليوم محتاجة قبعة تتحمل الشغل الحقيقي، مش بس تتصور في افتتاح. قبعات باكيت وسفاري وقبعات شمس عريضة، مريحة في حر مصر، للفرق الميدانية والفعاليات والحملات الموسمية.",
    image=None,
    page_title="Hats — REGINA Corporate Headwear",
    page_desc="Bucket, safari, and sun hats branded for outdoor teams, field staff, and seasonal campaigns.",
  ),
  "tshirts": dict(
    tag_en="Apparel", tag_ar="ملابس",
    title_en="T-Shirts", title_ar="تيشيرتات",
    desc_en="The tee your team actually wants to wear. Screen-printed or embroidered t-shirts for staff uniforms, product launches, and giveaways.",
    desc_ar="تيشيرت موظفينك هيلبسوه فعلاً كل يوم، مش بس يوم التصوير. قماش مريح، وطباعة أو تطريز نضيف، لزي الموظفين وإطلاق المنتجات والهدايا.",
    image=None,
    page_title="T-Shirts — REGINA Corporate Apparel",
    page_desc="Screen-printed and embroidered corporate t-shirts from REGINA for staff uniforms, launches, and giveaways.",
  ),
  "coverall": dict(
    tag_en="Workwear", tag_ar="ملابس عمل",
    title_en="Coverall", title_ar="الأوفرول",
    desc_en="Built for the shift, not the showroom. Heavy-duty industrial coveralls for factory, technical, and field teams — reinforced stitching, branded, sized per worker.",
    desc_ar="مصمم للشغل الحقيقي، مش للفاترينة. أوفرول شغل تقيل يتحمل شيفت كامل لفرق المصانع والفنيين — خياطة مقواة، بشعارك، وبمقاس كل فرد.",
    image="Coverall.jpg",
    page_title="Coverall — REGINA Industrial Workwear",
    page_desc="Heavy-duty branded coveralls from REGINA for industrial, technical, and field teams.",
  ),
  "graduation": dict(
    tag_en="Ceremonial", tag_ar="مناسبات",
    title_en="Graduation Gear", title_ar="زي التخرج",
    desc_en="One ceremony. Every gown fitting right. Gowns, caps, and sashes for schools and universities — produced to your institution's exact colors and sizing.",
    desc_ar="حفلة التخرج مالهاش إعادة… وكل ثوب لازم يبان مظبوط في كل صورة. أثواب وقبعات وأوشحة تخرج للمدارس والجامعات — بألوان ومقاسات مؤسستكم بالظبط.",
    image="Graduation.jpg",
    page_title="Graduation Gear — REGINA Ceremonial Wear",
    page_desc="Graduation gowns, caps, and sashes produced to your school or university's exact colors and sizing.",
  ),
}

for slug, data in CATEGORY_DATA.items():
    body = cat_body(slug, **{k: v for k, v in data.items() if k not in ("page_title", "page_desc")})
    out = page(data["page_title"], data["page_desc"], active_slug=slug, body_sections=body)
    write(f"{slug}.html", out)

print("All category pages generated.")
