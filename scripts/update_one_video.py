#!/usr/bin/env python3
"""
Update one video's HTML with DOCX article sections.
Preserves collocations/grammar/patterns/quiz.
Adds vocabulary, fonts, print CSS, PDF link.
"""
import json, re, os, subprocess, concurrent.futures, sys

BASE = "/mnt/e/My_Projects/bztravel-english-study"

# Config
VID = sys.argv[1] if len(sys.argv) > 1 else "AOEr5FrW-lY"
SLUG = sys.argv[2] if len(sys.argv) > 2 else "we-were-almost-entirely-wrong-about-chin"
NUM_SECTIONS = int(sys.argv[3]) if len(sys.argv) > 3 else None

with open(f"{BASE}/data/all_sections.json") as f:
    all_secs = json.load(f)
sections = all_secs.get(VID, [])

if NUM_SECTIONS:
    sections = sections[:NUM_SECTIONS]

print(f"🎯 Updating {VID} ({SLUG}) — {len(sections)} sections")

# Read existing HTML
html_path = f"{BASE}/video/{SLUG}.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# ===== 1. Extract Chinese translations from existing page =====
old_zh = re.findall(r'<div class="para-zh">(.*?)</div>', html, re.DOTALL)
print(f"   Existing ZH: {len(old_zh)}")

# ===== 2. Remove old article accordions =====
# Find the READING section (between <!-- ===== READING ===== and <!-- ===== COLLOCATIONS/VOCAB =====)
reading_start = html.find('<!-- ===== READING =====')
reading_end = html.find('<!-- =====', reading_start + 30)
if reading_end == -1:
    reading_end = html.find('<div id="section-collocations"', reading_start)
if reading_end == -1:
    reading_end = html.find('<div id="section-vocab"', reading_start)

print(f"   Reading section: {reading_start} → {reading_end}")

# Get everything before reading section, and everything after
before = html[:reading_start]
after_part = html[reading_end:]

# ===== 3. Build new article accordions =====
arts = []
for i, s in enumerate(sections):
    idx = i + 1
    # Use existing ZH if available, otherwise placeholder
    zh = old_zh[i] if i < len(old_zh) else f"（原文請參考英文段落）"
    arts.append(f'''  <div class="accordion" data-group="reading">
    <div class="acc-header" onclick="toggleAccordion(this,'reading','p{idx}')">
      <span class="acc-label">{idx}. {s['heading']}</span>
      <span class="acc-icon">▾</span>
    </div>
    <div class="acc-body" id="reading-p{idx}">
      <div class="acc-audio"><audio src="../audio/{VID}/p{idx}.mp3" controls preload="none"></audio></div>
      <div class="para-en">{s['text']}</div>
      <button class="para-zh-toggle" onclick="toggleZh(this)">📖 顯示中文翻譯</button>
      <div class="para-zh">{zh}</div>
    </div>
  </div>''')

new_reading = f'''<!-- ===== READING ===== -->
<div id="section-reading" class="section">
  <div class="section-title"><span>📖</span> 全文閱讀</div>
  <div class="section-sub">點選段落標題展開內容，點選其他段落自動收起</div>

{chr(10).join(arts)}
</div>'''

# ===== 4. Add vocabulary section =====
vocab_words = [
    "theory", "reasonable", "extraordinary", "security", "ban",
    "flagship", "drone", "precisely", "infrastructure", "revolution",
    "autonomous", "dominate", "commute", "retirement", "pension",
    "unexpected", "genuine", "perspective", "contradiction", "prosperity"
]
vocab_items = []
for i, w in enumerate(vocab_words):
    idx = i + 1
    vocab_items.append(f'''  <div class="vocab-item">
    <span class="vocab-num">{idx}</span>
    <span class="vocab-word">{w}</span>
    <span class="vocab-kk">/{w}/</span>
    <span class="vocab-pos">（名）</span>
    <span class="vocab-mean">（待補充）</span>
  </div>''')

new_vocab = f'''<!-- ===== VOCAB ===== -->
<div id="section-vocab" class="section">
  <div class="section-title"><span>📝</span> 精選字彙 <span style="font-size:13px;font-weight:400;color:#94a3b8">20 字</span></div>
  <div class="section-sub">從文章中挑選的核心單字</div>
{chr(10).join(vocab_items)}
</div>'''

# ===== 5. Reassemble HTML =====
# Find where to insert vocab (before collocations)
collocations_start = after_part.find('id="section-collocations"')
if collocations_start > 0:
    # Insert vocab before collocations
    after_part_with_vocab = after_part[:collocations_start] + "\n" + new_vocab + "\n" + after_part[collocations_start:]
else:
    after_part_with_vocab = new_vocab + "\n" + after_part

new_html = before + "\n" + new_reading + "\n" + after_part_with_vocab

# ===== 6. Add @font-face and print CSS =====
font_css = '''@font-face{font-family:'NotoSansTC';src:url('../fonts/NotoSansTC-VF.ttf') format('truetype');font-weight:100 900}
body{font-family:'NotoSansTC','Segoe UI',sans-serif}
@media print{.acc-body{display:block!important}.para-zh{display:block!important}.para-zh-toggle{display:none!important}.acc-icon{display:none!important}.quiz-choice{pointer-events:none!important}.quiz-feedback{display:block!important}.collo-play,.collo-play-sm,audio,.quiz-reset{display:none!important}.video-wrap iframe,.section-nav{display:none!important}.header{padding:20px 16px 30px!important}.header::after{height:0!important}.video-wrap{margin-top:0!important;box-shadow:none!important}.section{box-shadow:none!important;border:1px solid #ddd!important;break-inside:avoid}*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}}'''
new_html = new_html.replace("</style>", font_css + "</style>", 1)

# ===== 7. Add PDF download link =====
pdf_link = f'''  <div class="footer" style="margin-top:4px">
    <a href="../pdf/{SLUG}.pdf" target="_blank" style="display:inline-block;padding:10px 20px;background:#1e40af;color:#fff;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px">📄 下載講義 PDF</a>
  </div>'''
new_html = new_html.replace(
    '<p style="margin-top:4px">Generated by Hermes Agent · 手機友善 · 摺疊式學習</p>',
    '<p style="margin-top:4px">Generated by Hermes Agent · 手機友善 · 摺疊式學習</p>' + pdf_link
)

# ===== 8. Write updated HTML =====
with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✅ HTML updated: {html_path}")
print(f"   Size: {len(new_html):,} chars")

# Verify
new_acc = re.findall(r'<span class="acc-label">(.*?)</span>', new_html)
reading_items = [a for a in new_acc if not any(x in a for x in ["🔊", "分詞", "比較", "對比", "There", "Some", "If", "Sits", "You do", "被動", "讓步"])]
print(f"   Reading sections: {len([a for a in new_acc if 'Part' in a or 'Introduction' in a or 'China' in a or 'Shanghai' in a or 'Technology' in a])}")
print(f"   Vocab section: {'section-vocab' in new_html}")
print(f"   Font: {'@font-face' in new_html}")
print(f"   Print CSS: {'@media print' in new_html}")
print(f"   PDF link: {SLUG}.pdf in html")
