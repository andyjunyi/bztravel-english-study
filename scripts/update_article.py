#!/usr/bin/env python3
"""Replace article section in one video page with DOCX content."""
import json, re, os, sys

BASE = "/mnt/e/My_Projects/bztravel-english-study"

VID = sys.argv[1]
SLUG = sys.argv[2]

with open(f"{BASE}/data/all_sections.json") as f:
    all_secs = json.load(f)
sections = all_secs.get(VID, [])

html_path = f"{BASE}/video/{SLUG}.html"
with open(html_path) as f:
    html = f.read()

# Find reading section boundaries
rs = html.find('<div id="section-reading"')
re_block = html.find('<div id="section-collocations"', rs)
if re_block == -1:
    re_block = html.find('<div id="section-vocab"', rs)
if re_block == -1:
    re_block = html.find('<!-- =====', rs + 10)

# Extract old ZH translations from within the reading section
old_reading = html[rs:re_block]
old_zh = re.findall(r'<div class="para-zh">(.*?)</div>', old_reading, re.DOTALL)
print(f"Existing ZH: {len(old_zh)}, New sections: {len(sections)}")

# Build new reading section
arts = []
for i, s in enumerate(sections):
    idx = i + 1
    zh = old_zh[i] if i < len(old_zh) else "（翻譯待更新）"
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

new_reading = f'''<div id="section-reading" class="section">
  <div class="section-title"><span>📖</span> 全文閱讀</div>
  <div class="section-sub">點選段落標題展開內容，點選其他段落自動收起</div>
{chr(10).join(arts)}
</div>'''

# Replace reading section
new_html = html[:rs] + new_reading + html[re_block:]

# Add vocab section (before collocations)
vocab_data = [
    ("theory","/ˈθɪri/","名","理論；說法"), ("reasonable","/ˈrizənəbəl/","形","合理的"),
    ("extraordinary","/ɪkˈstrɔrdəˌnɛri/","形","非凡的"), ("security","/səˈkjʊrəti/","名","安全；保全"),
    ("flagship","/ˈflæɡˌʃɪp/","名","旗艦店"), ("drone","/droʊn/","名","無人機"),
    ("precisely","/prɪˈsaɪsli/","副","精確地"), ("infrastructure","/ˈɪnfrəˌstrʌktʃər/","名","基礎建設"),
    ("revolution","/ˌrɛvəˈluʃən/","名","革命"), ("autonomous","/ɔˈtɑnəməs/","形","自動的；自主的"),
    ("dominate","/ˈdɑməˌnet/","動","主導；支配"), ("commute","/kəˈmjut/","名/動","通勤"),
    ("retirement","/rɪˈtaɪərmənt/","名","退休"), ("pension","/ˈpɛnʃən/","名","退休金；養老金"),
    ("unexpected","/ˌʌnɪkˈspɛktɪd/","形","出乎意料的"), ("genuine","/ˈdʒɛnjuɪn/","形","真誠的；真正的"),
    ("perspective","/pərˈspɛktɪv/","名","觀點；視角"), ("contradiction","/ˌkɑntrəˈdɪkʃən/","名","矛盾"),
    ("prosperity","/prɑˈspɛrəti/","名","繁榮"), ("unfiltered","/ʌnˈfɪltɚd/","形","未過濾的；真實的"),
]
vocab_items = []
for i, (w, kk, pos, mean) in enumerate(vocab_data):
    vocab_items.append(f'  <div class="vocab-item"><span class="vocab-num">{i+1}</span><span class="vocab-word">{w}</span><span class="vocab-kk">{kk}</span><span class="vocab-pos">（{pos}）</span><span class="vocab-mean">{mean}</span></div>')

new_vocab = f'''<div id="section-vocab" class="section">
  <div class="section-title"><span>📝</span> 精選字彙 <span style="font-size:13px;font-weight:400;color:#94a3b8">20 字</span></div>
  <div class="section-sub">從文章中挑選的核心單字</div>
{chr(10).join(vocab_items)}
</div>

'''

# Insert vocab before collocations
collo_pos = new_html.find('id="section-collocations"')
if collo_pos > 0:
    new_html = new_html[:collo_pos] + new_vocab + new_html[collo_pos:]

# Add @font-face + print CSS
extra_css = '\n@font-face{font-family:NotoSansTC;src:url(../fonts/NotoSansTC-VF.ttf) format(truetype);font-weight:100 900}\nbody{font-family:NotoSansTC,Segoe UI,sans-serif}\n@media print{.acc-body{display:block!important}.para-zh{display:block!important}.para-zh-toggle{display:none!important}.acc-icon{display:none!important}.quiz-choice{pointer-events:none!important}.quiz-feedback{display:block!important}.collo-play,.collo-play-sm,audio,.quiz-reset{display:none!important}.video-wrap iframe,.section-nav{display:none!important}.header{padding:20px 16px 30px!important}.header::after{height:0!important}.video-wrap{margin-top:0!important;box-shadow:none!important}.section{box-shadow:none!important;border:1px solid #ddd!important;break-inside:avoid}*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}}'
if '@font-face' not in new_html:
    new_html = new_html.replace('</style>', extra_css + '</style>', 1)

# Add PDF download link
pdf_link = f'\n  <div class="footer" style="margin-top:4px">\n    <a href="../pdf/{SLUG}.pdf" target="_blank" style="display:inline-block;padding:10px 20px;background:#1e40af;color:#fff;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px">📄 下載講義 PDF</a>\n  </div>'
if '../pdf/' + SLUG + '.pdf' not in new_html:
    new_html = new_html.replace(
        '<p style="margin-top:4px">Generated by Hermes Agent · 手機友善 · 摺疊式學習</p>',
        '<p style="margin-top:4px">Generated by Hermes Agent · 手機友善 · 摺疊式學習</p>' + pdf_link
    )

# Write
with open(html_path, "w") as f:
    f.write(new_html)

# Verify
import re as regex
accs = regex.findall(r'<span class="acc-label">(.*?)</span>', new_html)
reading = [a for a in accs if not any(x in a for x in ["🔊","分詞","比較","對比","There","Some","If","Sits","You do","被動","讓步","build","crumble","keep","political","reasonable","more","state","miss"]) and len(a) < 50]
print(f"✅ Updated: {VID}")
print(f"   Article: {len(reading)} sections")
print(f"   Collocations: {'data-group=collo' in new_html}")
print(f"   Grammar: {'data-group=grammar' in new_html}")
print(f"   Patterns: {'data-group=pattern' in new_html}")
print(f"   Quiz: {'QUIZ' in new_html}")
print(f"   Vocab: {new_html.count('vocab-item')} words")
print(f"   Font+Print: {'@font-face' in new_html}")
