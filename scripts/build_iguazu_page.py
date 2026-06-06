#!/usr/bin/env python3
"""Generate updated Iguazu Falls HTML page from DOCX reference."""
import json, os

BASE = "/mnt/e/My_Projects/bztravel-english-study"
VID = "xW5SlCvx2W0"
AP = f"../audio/{VID}"

with open(f"{BASE}/data/iguazu_new_sections.json") as f:
    sections = json.load(f)
with open(f"{BASE}/data/iguazu_zh_translations.json") as f:
    zh_trans = json.load(f)

# ===== Build article accordion =====
def article_html():
    items = []
    for i, (s, zh) in enumerate(zip(sections, zh_trans)):
        idx = i + 1
        items.append(f'''    <div class="accordion" data-group="reading">
      <div class="acc-header" onclick="toggleAccordion(this,'reading','p{idx}')">
        <span class="acc-label">{idx}. {s['heading']}</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="reading-p{idx}">
        <div class="acc-audio"><audio src="{AP}/p{idx}.mp3" controls preload="none"></audio></div>
        <div class="para-en">{s['text']}</div>
        <button class="para-zh-toggle" onclick="toggleZh(this)">📖 顯示中文翻譯</button>
        <div class="para-zh">{zh}</div>
      </div>
    </div>''')
    return "\n".join(items)

# ===== Vocabulary =====
vocab = [
    ("silence", "/ˈsaɪləns/", "動", "使沉默；使安靜"),
    ("speechless", "/ˈspitʃləs/", "形", "說不出話的"),
    ("border", "/ˈbɔrdɚ/", "名", "邊界"),
    ("panoramic", "/ˌpænəˈræmɪk/", "形", "全景的"),
    ("gradual", "/ˈgrædʒuəl/", "形", "漸進的"),
    ("reveal", "/rɪˈvil/", "動", "展現；揭露"),
    ("sheer", "/ʃɪr/", "形", "完全的；陡峭的"),
    ("scattered", "/ˈskætɚd/", "形", "散布的"),
    ("prepare", "/prɪˈpɛr/", "動", "準備"),
    ("radical", "/ˈrædɪkəl/", "形", "激進的；徹底的"),
    ("elevated", "/ˈɛləˌvetɪd/", "形", "高架的"),
    ("affordable", "/əˈfɔrdəbəl/", "形", "負擔得起的"),
    ("converge", "/kənˈvɝdʒ/", "動", "匯聚"),
    ("plunge", "/plʌndʒ/", "動", "墜落"),
    ("overwhelming", "/ˌovɚˈwɛlmɪŋ/", "形", "壓倒性的"),
    ("terrifying", "/ˈtɛrəˌfaɪɪŋ/", "形", "令人恐懼的"),
    ("deafening", "/ˈdɛfənɪŋ/", "形", "震耳欲聾的"),
    ("extraordinary", "/ɪkˈstrɔrdəˌnɛri/", "形", "非凡的；卓越的"),
    ("thrilling", "/ˈθrɪlɪŋ/", "形", "令人興奮的"),
    ("breathtaking", "/ˈbrɛθˌtekɪŋ/", "形", "令人屏息的"),
]

def vocab_html():
    items = []
    for i, (word, kk, pos, meaning) in enumerate(vocab):
        idx = i + 1
        items.append(f'''    <div class="vocab-item">
      <span class="vocab-num">{idx}</span>
      <span class="vocab-word">{word}</span>
      <span class="vocab-kk">{kk}</span>
      <span class="vocab-pos">（{pos}）</span>
      <span class="vocab-mean">{meaning}</span>
    </div>''')
    return "\n".join(items)

# ===== Collocations HTML =====
collos = [
    {"phrase": "leave someone speechless", "audio": "collo1",
     "meaning": "讓某人說不出話來（震驚到無法言語）",
     "example": '"There are places in this world that silence you the moment you arrive."',
     "example_zh": "世界上有些地方，你一到達就會被震懾得說不出話來。",
     "ex_audio": "ex1"},
    {"phrase": "sheer overwhelming scale", "audio": "collo2",
     "meaning": "壓倒性的規模；極其龐大的尺度",
     "example": '"The biggest surprise was the sheer overwhelming scale of it all."',
     "example_zh": "最大的驚喜是那壓倒性的規模。",
     "ex_audio": "ex2"},
    {"phrase": "as far as the eye can see", "audio": "collo3",
     "meaning": "一望無際；視線所及之處",
     "example": '"275 individual falls scattered across the jungle as far as the eye could see."',
     "example_zh": "275條瀑布散布在叢林中，一望無際。",
     "ex_audio": "ex3"},
    {"phrase": "pressing in from every side", "audio": "collo4",
     "meaning": "從四面八方逼近／湧來",
     "example": '"The jungle pressing in, water moving fast beneath your feet."',
     "example_zh": "叢林從兩側逼近，腳下水流湍急。",
     "ex_audio": "ex4"},
    {"phrase": "borders on frightening", "audio": "collo5",
     "meaning": "近乎令人害怕",
     "example": '"Raw, deafening, alive in a way that borders on frightening."',
     "example_zh": "原始、震耳欲聾、充滿生命力，近乎令人害怕。",
     "ex_audio": "ex5"},
    {"phrase": "beyond description", "audio": "collo6",
     "meaning": "難以形容",
     "example": '"Some things exist beyond description. This is one of them."',
     "example_zh": "有些事情存在於言語之外。這就是其中之一。",
     "ex_audio": "ex6"},
    {"phrase": "hammer against", "audio": "collo7",
     "meaning": "猛烈衝擊；猛力撞擊",
     "example": '"The boat hammers against the current at full speed."',
     "example_zh": "船隻以全速逆流衝擊。",
     "ex_audio": "ex7"},
    {"phrase": "hit like a wall", "audio": "collo8",
     "meaning": "像牆一樣迎面襲來",
     "example": '"Noise, white water, cold, hitting like a wall."',
     "example_zh": "噪音、白水、和像牆一樣撞擊過來的冰冷。",
     "ex_audio": "ex8"},
]

def collo_html():
    items = []
    for i, c in enumerate(collos):
        idx = i + 1
        items.append(f'''    <div class="accordion" data-group="collo">
      <div class="acc-header" onclick="toggleAccordion(this,'collo','c{idx}')">
        <span class="acc-label">{idx}. {c['phrase']} <span class="collo-play" onclick="event.stopPropagation();playCollo('{c['audio']}')">🔊</span></span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="collo-c{idx}">
        <div class="collo-meaning">{c['meaning']}</div>
        <div class="collo-example">
          <span class="label">📌 文中例句</span><br>
          <div class="collo-en">{c['example']} <span class="collo-play-sm" onclick="playCollo('{c['ex_audio']}')">🔊</span></div>
          <div class="collo-zh">{c['example_zh']}</div>
        </div>
      </div>
    </div>''')
    return "\n".join(items)

# ===== Grammar HTML =====
def grammar_html():
    return '''    <div class="accordion" data-group="grammar">
      <div class="acc-header" onclick="toggleAccordion(this,'grammar','g1')">
        <span class="acc-label">分詞構句 — V-ing 開頭表伴隨情況</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="grammar-g1">
        <div class="grammar-explain">分詞構句（Participle Phrase）可以將兩個相關的動作或狀態合併成一句，讓句子更簡潔優雅。當主句和附屬句的主詞相同時，附屬句的動詞改為 V-ing 形式。</div>
        <div class="grammar-examples">
          <div class="ge-item">
            <div class="ge-from">▸ "Having seen Niagara and stood at the misty edge of Victoria Falls, they arrived expecting something roughly the same."</div>
            <div class="ge-zh">去過尼加拉瀑布、站過維多利亞瀑布霧氣瀰漫的邊緣之後，他們抵達時心裡預期的大概差不多就是那樣。</div>
            <div class="ge-analysis">→ 'Having seen...' = After they had seen...（完成式分詞構句，強調先發生）<br>→ 'expecting...' = and they expected...（簡單分詞構句，表伴隨狀態）</div>
            <div class="ge-pattern">Having + p.p. + ..., S + V ... → 完成某事之後，主詞做...</div>
          </div>
          <div class="ge-item">
            <div class="ge-from">▸ "The boat hammers against the current, throwing you over rapids."</div>
            <div class="ge-zh">船隻以全速逆流衝擊，將你拋過急流。</div>
            <div class="ge-analysis">→ 'throwing you over rapids' = and it throws you over rapids<br>→ 表伴隨結果：主動作造成的副效果</div>
            <div class="ge-pattern">S + V + O, V-ing + O → 主詞做某事，因而產生...</div>
          </div>
        </div>
      </div>
    </div>

    <div class="accordion" data-group="grammar">
      <div class="acc-header" onclick="toggleAccordion(this,'grammar','g2')">
        <span class="acc-label">比較結構 — 否定詞 + 比較級</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="grammar-g2">
        <div class="grammar-explain">用否定詞（nothing, no, never）+ 比較級，可以表達「沒有什麼比...更...」的超級最高級意味，比直接使用最高級更有強調效果。</div>
        <div class="grammar-examples">
          <div class="ge-item">
            <div class="ge-from">▸ "Nothing — not a photograph, not a travel blog, not a single video — prepares you for what Iguazu actually is."</div>
            <div class="ge-zh">沒有什麼——不是照片、不是旅遊部落格、不是任何影片——能讓你準備好面對伊瓜蘇的真正面貌。</div>
            <div class="ge-analysis">→ 用三個 not 排比強調「沒有任何方式能讓你準備好」<br>→ 比直接說 'No one can prepare you' 更有感染力</div>
            <div class="ge-pattern">Nothing / No + N + ... 強調「沒有任何...能...」</div>
          </div>
          <div class="ge-item">
            <div class="ge-from">▸ "None of them come close."</div>
            <div class="ge-zh">沒有任何一個能相提並論。</div>
            <div class="ge-analysis">→ 'none... come close' = 沒有任何一個能相提並論<br>→ 口語中極高頻的比較否定用法</div>
            <div class="ge-pattern">None come close = 無人能及</div>
          </div>
        </div>
      </div>
    </div>

    <div class="accordion" data-group="grammar">
      <div class="acc-header" onclick="toggleAccordion(this,'grammar','g3')">
        <span class="acc-label">對比平行結構 — At X..., at Y..., at Z...</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="grammar-g3">
        <div class="grammar-explain">使用三個以上平行的對比結構，可以強化差異、製造韻律感，是英文寫作中的華麗修辭手法（排比 / parallel structure）。</div>
        <div class="grammar-examples">
          <div class="ge-item">
            <div class="ge-from">▸ "At Niagara, you watch from across a river. At Victoria, from across a gorge. At Iguazu, there is no across."</div>
            <div class="ge-zh">在尼加拉，你隔著河流觀看。在維多利亞，你隔著峽谷觀看。在伊瓜蘇，沒有所謂的「對面」。</div>
            <div class="ge-analysis">→ 三個 'At...' 開頭，前兩個描述其他瀑布的相似點<br>→ 第三個反轉（'there is no across'），達到強烈對比效果</div>
            <div class="ge-pattern">At [A]..., at [B]..., at [C]... (反轉) — 排比對比修辭</div>
          </div>
        </div>
      </div>
    </div>'''

# ===== Patterns HTML =====
def patterns_html():
    return '''    <div class="accordion" data-group="pattern">
      <div class="acc-header" onclick="toggleAccordion(this,'pattern','pt1')">
        <span class="acc-label">There are [places/things] in this world that + V...</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="pattern-pt1">
        <div class="pattern-meaning">世界上有些地方...（強烈推薦的開場句）</div>
        <div class="pattern-example">📌 "There are places in this world that silence you the moment you arrive."</div>
        <div class="pattern-example-zh">世界上有些地方，你一到達就會被震懾得說不出話來。</div>
        <div class="pattern-template">📐 There are [places/things/people] in this world that [描述] you the moment you [動詞].</div>
      </div>
    </div>

    <div class="accordion" data-group="pattern">
      <div class="acc-header" onclick="toggleAccordion(this,'pattern','pt2')">
        <span class="acc-label">Some things exist beyond... / No words are adequate for...</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="pattern-pt2">
        <div class="pattern-meaning">無法用言語形容（表達極致感受）</div>
        <div class="pattern-example">📌 "We wish we had better words. We do not. Some things exist beyond description."</div>
        <div class="pattern-example-zh">但願我們有更好的詞彙。我們沒有。有些事情存在於言語之外。</div>
        <div class="pattern-template">📐 No words are adequate for [名詞]. / Some things exist beyond [名詞].</div>
      </div>
    </div>

    <div class="accordion" data-group="pattern">
      <div class="acc-header" onclick="toggleAccordion(this,'pattern','pt3')">
        <span class="acc-label">If it's not on your [名詞], it needs to be.</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="pattern-pt3">
        <div class="pattern-meaning">如果不在你的...清單上，它應該要在（強烈推薦）</div>
        <div class="pattern-example">📌 "If it's not on your bucket list, it needs to be."</div>
        <div class="pattern-example-zh">如果它還不在你的願望清單上，它應該要在。</div>
        <div class="pattern-template">📐 If [事物] is not on your [list/schedule/radar], it needs to be.</div>
      </div>
    </div>

    <div class="accordion" data-group="pattern">
      <div class="acc-header" onclick="toggleAccordion(this,'pattern','pt4')">
        <span class="acc-label">Sits above all others with nothing close behind.</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="pattern-pt4">
        <div class="pattern-meaning">遙遙領先，後無來者（最高級強調句）</div>
        <div class="pattern-example">📌 "The one that sits above all others with nothing close behind."</div>
        <div class="pattern-example-zh">穩坐第一，後無來者。</div>
        <div class="pattern-template">📐 [事物] sits above all others with nothing close behind.</div>
      </div>
    </div>

    <div class="accordion" data-group="pattern">
      <div class="acc-header" onclick="toggleAccordion(this,'pattern','pt5')">
        <span class="acc-label">You do not [A] it — you [B] it, and you let it [C] you.</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="pattern-pt5">
        <div class="pattern-meaning">否定→轉折強調的修辭手法</div>
        <div class="pattern-example">📌 "You do not admire it. You stand inside it, soaked through, and you let it happen to you."</div>
        <div class="pattern-example-zh">你不是在欣賞它——你站在它裡面，全身濕透，讓它衝擊你。</div>
        <div class="pattern-template">📐 You do not [消極動詞] it — you [積極動詞] it, and you let it [動詞] you.</div>
      </div>
    </div>'''

# ===== Quiz JS =====
quiz_js = '''var QUIZ = [
  {q:"What is the main purpose of this video?", choices:["To compare Iguazu Falls with other famous waterfalls","To describe the experience of visiting Iguazu Falls from multiple perspectives","To explain how Iguazu Falls was formed geologically","To give practical travel tips for visiting Brazil and Argentina"], answer:1, explain:"The video shows Iguazu from every angle — the Brazilian side, the Argentine side, from the air in a helicopter, and from the water in a speedboat — all to convey the full experience."},
  {q:"What does the phrase 'there is no across' at Iguazu Falls mean?", choices:["You cannot see the falls from the opposite side","The falls are too wide to see across","The walkways take you directly into the waterfall rather than letting you watch from a distance","The border between Brazil and Argentina blocks the view"], answer:2, explain:"'At other waterfalls, you stand across... at Iguazu, there is no across.' The bridge takes you into the water, not around it. You are 'inside a waterfall.'"},
  {q:"The word 'sheer' in 'the sheer overwhelming scale' is closest in meaning to:", choices:["thin and transparent","complete and total","steep and vertical","surprising and unexpected"], answer:1, explain:"Here, 'sheer' means 'complete and total' — a common intensifier: sheer luck, sheer terror, sheer beauty."},
  {q:"How does the narrator create contrast between Iguazu and other waterfalls?", choices:["By listing the heights of different waterfalls","By using a parallel structure: 'At Niagara... At Victoria... At Iguazu...'","By showing photographs of each waterfall","By interviewing tourists about their experiences"], answer:1, explain:"The parallel structure (排比) — 'At Niagara... At Victoria... At Iguazu...' — creates rhythm and emphasizes Iguazu's uniqueness."},
  {q:"Which best captures the overall feeling of the video?", choices:["Iguazu Falls is an affordable travel destination.","Iguazu Falls is an experience that cannot be fully described in words.","The Brazilian side is better than the Argentine side.","The helicopter ride is the best part."], answer:1, explain:"The narrator repeatedly says: 'We wish we had better words. We do not. Some things exist beyond description. This is one of them.'"}
];'''

# ===== Build full HTML =====
html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>Iguazu Falls — 英文自學講義 | BZ Travel</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{
  background:#f0f4ff;color:#1e293b;
  font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
  max-width:100vw;overflow-x:hidden;
  line-height:1.6;
}}
.header{{
  background:linear-gradient(135deg,#0c4a6e,#1e40af,#3b82f6);
  padding:20px 16px 60px;position:relative;color:#fff;text-align:center;
}}
.header::after{{
  content:'';position:absolute;bottom:-1px;left:0;right:0;
  height:30px;background:#f0f4ff;border-radius:30px 30px 0 0;
}}
.header-badge{{
  display:inline-block;background:rgba(255,255,255,.15);
  padding:4px 14px;border-radius:20px;
  font-size:12px;letter-spacing:1px;margin-bottom:10px;
}}
.header h1{{font-size:22px;font-weight:700;margin-bottom:4px;line-height:1.3}}
.header .sub{{font-size:14px;opacity:.85}}
.header-meta{{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:10px;font-size:13px;opacity:.9}}
.main-wrap{{max-width:800px;margin:0 auto;padding:0 16px 100px}}
.video-wrap{{
  position:relative;margin-top:-40px;z-index:2;
  border-radius:16px;overflow:hidden;
  box-shadow:0 8px 30px rgba(0,0,0,.15);background:#000;
}}
.video-wrap iframe{{display:block;width:100%;aspect-ratio:16/9;border:none}}
.section{{border-radius:16px;background:#fff;padding:20px;margin-bottom:14px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.section-title{{font-size:17px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:8px}}
.section-sub{{font-size:12px;color:#94a3b8;margin-bottom:14px}}
.accordion{{border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;margin-bottom:8px}}
.accordion:last-child{{margin-bottom:0}}
.acc-header{{
  display:flex;align-items:center;justify-content:space-between;
  padding:12px 14px;cursor:pointer;
  background:#fafafa;transition:all .2s;user-select:none;
  gap:8px;
}}
.acc-header:hover{{background:#eff6ff}}
.acc-header.open{{background:#eff6ff;border-bottom:1px solid #e2e8f0}}
.acc-header .acc-label{{font-size:14px;font-weight:600;flex:1;line-height:1.3}}
.acc-header .acc-icon{{
  flex-shrink:0;width:22px;height:22px;border-radius:50%;
  background:#e2e8f0;color:#64748b;
  display:flex;align-items:center;justify-content:center;
  font-size:13px;font-weight:700;transition:all .3s;
}}
.acc-header.open .acc-icon{{background:#1e40af;color:#fff;transform:rotate(180deg)}}
.acc-body{{display:none;padding:14px;background:#fff;animation:fadeIn .2s ease}}
.acc-body.open{{display:block}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(-4px)}}to{{opacity:1;transform:translateY(0)}}}}
.acc-audio{{margin-bottom:8px}}
.acc-audio audio{{width:100%;height:34px;border-radius:6px}}
.para-en{{font-size:14.5px;line-height:1.8;color:#1e293b;margin-bottom:10px}}
.para-zh-toggle{{
  display:inline-flex;align-items:center;gap:4px;
  font-size:12px;font-weight:600;color:#3b82f6;cursor:pointer;
  background:#eff6ff;padding:5px 12px;border-radius:6px;border:none;margin-bottom:8px;
}}
.para-zh{{
  display:none;font-size:14px;color:#64748b;line-height:1.8;
  padding:10px 12px;background:#f8fafc;border-radius:8px;border-left:3px solid #3b82f6;
}}
.vocab-item{{
  display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;
  padding:8px 0;border-bottom:1px solid #e2e8f0;
}}
.vocab-item:last-child{{border-bottom:none}}
.vocab-num{{font-size:11px;color:#94a3b8;font-weight:600;width:20px;flex-shrink:0}}
.vocab-word{{font-size:15px;font-weight:700;color:#1e293b}}
.vocab-kk{{font-size:13px;color:#be123c;font-family:'Arial Unicode MS','Segoe UI',sans-serif}}
.vocab-pos{{font-size:12px;color:#64748b;background:#f1f5f9;padding:1px 6px;border-radius:4px}}
.vocab-mean{{font-size:14px;color:#334155}}
.collo-phrase{{font-size:15px;font-weight:700;color:#1e40af}}
.collo-meaning{{font-size:13px;color:#64748b;margin-bottom:8px}}
.collo-example{{font-size:13px;color:#334155;background:#f8fafc;padding:8px 10px;border-radius:6px;margin-bottom:6px;border-left:3px solid #10b981}}
.collo-example .label{{font-weight:600;color:#10b981;font-size:11px}}
.collo-en{{margin-bottom:4px;line-height:1.6}}
.collo-zh{{color:#059669;font-size:12.5px;line-height:1.6;padding:4px 8px;background:#ecfdf5;border-radius:4px;display:inline-block}}
.collo-play,.collo-play-sm{{
  display:inline-flex;align-items:center;justify-content:center;
  cursor:pointer;transition:all .2s;border-radius:50%;
  flex-shrink:0;
}}
.collo-play{{width:28px;height:28px;font-size:14px;background:rgba(30,64,175,.1);vertical-align:middle;margin-left:4px}}
.collo-play:active{{background:#1e40af;transform:scale(.9)}}
.collo-play-sm{{width:24px;height:24px;font-size:12px;background:rgba(16,185,129,.1);vertical-align:middle;margin-left:3px}}
.collo-play-sm:active{{background:#10b981;transform:scale(.9)}}
.grammar-point{{font-size:15px;font-weight:700;color:#7c3aed}}
.grammar-explain{{font-size:13px;color:#64748b;margin-bottom:10px;line-height:1.6}}
.grammar-examples{{background:#f5f3ff;border-radius:8px;padding:10px 12px;margin-bottom:10px}}
.ge-item{{margin-bottom:12px}}
.ge-item:last-child{{margin-bottom:0}}
.ge-from{{font-size:13px;color:#6d28d9;font-style:italic;margin-bottom:2px}}
.ge-zh{{font-size:12.5px;color:#7c3aed;line-height:1.6;padding:4px 8px;background:#ede9fe;border-radius:4px;margin-bottom:6px;display:inline-block}}
.ge-analysis{{font-size:12px;color:#475569;line-height:1.5}}
.ge-analysis br{{display:block;content:'';margin-top:4px}}
.ge-pattern{{font-size:12px;color:#7c3aed;font-weight:600;margin-top:2px;padding:3px 8px;background:#ede9fe;border-radius:4px;display:inline-block}}
.pattern-meaning{{font-size:13px;color:#64748b;margin-bottom:6px}}
.pattern-example{{font-size:13px;color:#334155;background:#ecfeff;padding:8px 10px;border-radius:6px;margin-bottom:4px;border-left:3px solid #06b6d4;line-height:1.6}}
.pattern-example-zh{{font-size:12.5px;color:#0e7490;background:#cffafe;padding:4px 10px;border-radius:4px;margin-bottom:6px;display:inline-block;line-height:1.6}}
.pattern-template{{font-size:12px;color:#0891b2;font-weight:600;background:#ecfeff;padding:4px 8px;border-radius:4px;display:inline-block}}
.quiz-question{{border:1px solid #e2e8f0;border-radius:12px;padding:14px;margin-bottom:12px;transition:all .3s}}
.quiz-q{{font-size:15px;font-weight:600;margin-bottom:8px;line-height:1.5}}
.quiz-choices{{display:grid;gap:6px}}
.quiz-choice{{padding:10px 14px;border:2px solid #e2e8f0;border-radius:10px;font-size:14px;cursor:pointer;transition:all .2s;background:#fafafa}}
.quiz-choice:hover{{border-color:#93c5fd;background:#eff6ff}}
.quiz-choice.selected{{border-color:#3b82f6;background:#dbeafe;font-weight:600}}
.quiz-choice.correct{{border-color:#059669;background:#d1fae5;color:#065f46}}
.quiz-choice.wrong{{border-color:#dc2626;background:#fef2f2;color:#991b1b}}
.quiz-feedback{{display:none;margin-top:10px;padding:10px 12px;border-radius:8px;font-size:13px;line-height:1.6}}
.quiz-feedback.show{{display:block}}
.quiz-feedback.correct{{background:#d1fae5;border-left:4px solid #059669;color:#065f46}}
.quiz-feedback.wrong{{background:#fef2f2;border-left:4px solid #dc2626;color:#991b1b}}
.quiz-score{{text-align:center;padding:14px;font-size:17px;font-weight:700;background:#f0f4ff;border-radius:12px;margin-bottom:14px}}
.quiz-reset{{display:block;width:100%;padding:12px;border:none;border-radius:10px;background:#e2e8f0;color:#475569;font-size:15px;font-weight:600;cursor:pointer;transition:all .2s;margin-top:4px}}
.quiz-reset:hover{{background:#cbd5e1}}
.section-nav{{display:flex;gap:6px;overflow-x:auto;padding:14px 0 8px;margin-bottom:2px;-webkit-overflow-scrolling:touch;scrollbar-width:none}}
.section-nav::-webkit-scrollbar{{display:none}}
.section-nav a{{flex-shrink:0;padding:7px 16px;border-radius:20px;font-size:13px;font-weight:600;text-decoration:none;background:#e2e8f0;color:#475569;transition:all .2s;white-space:nowrap}}
.section-nav a:hover,.section-nav a.active{{background:#1e40af;color:#fff}}
.footer{{text-align:center;padding:30px 16px 20px;font-size:13px;color:#94a3b8}}
.footer a{{color:#3b82f6;text-decoration:none}}
@media(max-width:480px){{.header h1{{font-size:18px}}.section{{padding:14px}}.acc-header{{padding:10px 12px}}}}
</style>
</head>
<body>

<div class="header">
  <div class="header-badge">🌎 BZ Travel · 英文自學講義</div>
  <h1>Iguazu Falls: The Most Powerful Waterfall on Earth</h1>
  <div class="sub">從巴西到阿根廷，體驗地球上最震撼的瀑布</div>
  <div class="header-meta">
    <span>⏱️ 17:05</span>
    <span>🌍 巴西 / 阿根廷</span>
    <span>🏷️ 自然奇景</span>
  </div>
</div>

<div class="main-wrap">

  <div class="video-wrap">
    <iframe src="https://www.youtube.com/embed/{VID}" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>

  <div class="section-nav">
    <a href="#section-reading" class="active">📖 閱讀</a>
    <a href="#section-vocab">📝 字彙</a>
    <a href="#section-collocations">🔗 搭配詞</a>
    <a href="#section-grammar">📐 文法</a>
    <a href="#section-patterns">🧩 句型</a>
    <a href="#section-quiz">📝 測驗</a>
  </div>

  <!-- ===== READING ===== -->
  <div id="section-reading" class="section">
    <div class="section-title"><span>📖</span> 全文閱讀</div>
    <div class="section-sub">點選段落標題展開內容，點選其他段落自動收起</div>

{article_html()}
  </div>

  <!-- ===== VOCABULARY ===== -->
  <div id="section-vocab" class="section">
    <div class="section-title"><span>📝</span> 精選字彙 <span style="font-size:13px;font-weight:400;color:#94a3b8">20 字</span></div>
    <div class="section-sub">從文章中挑選的核心單字</div>

{vocab_html()}
  </div>

  <!-- ===== COLLOCATIONS ===== -->
  <div id="section-collocations" class="section">
    <div class="section-title"><span>🔗</span> 實用搭配詞 <span style="font-size:13px;font-weight:400;color:#94a3b8">8 組</span></div>
    <div class="section-sub">點選搭配詞展開完整內容</div>

{collo_html()}
  </div>

  <!-- ===== GRAMMAR ===== -->
  <div id="section-grammar" class="section">
    <div class="section-title"><span>📐</span> 文法重點 <span style="font-size:13px;font-weight:400;color:#94a3b8">3 點</span></div>
    <div class="section-sub">點選文法點展開完整說明</div>

{grammar_html()}
  </div>

  <!-- ===== PATTERNS ===== -->
  <div id="section-patterns" class="section">
    <div class="section-title"><span>🧩</span> 關鍵句型 <span style="font-size:13px;font-weight:400;color:#94a3b8">5 組</span></div>
    <div class="section-sub">點選句型展開範例與練習</div>

{patterns_html()}
  </div>

  <!-- ===== QUIZ ===== -->
  <div id="section-quiz" class="section">
    <div class="section-title"><span>📝</span> 閱讀測驗 <span style="font-size:13px;font-weight:400;color:#94a3b8">5 題</span></div>
    <div class="section-sub">點選答案即時對答</div>
    <div id="quizContainer"></div>
  </div>

  <div class="footer">
    <p>📺 影片來源：<a href="https://youtube.com/@bztravel" target="_blank">BZ Travel</a></p>
    <p style="margin-top:4px">Generated by Hermes Agent · 手機友善 · 摺疊式學習</p>
  </div>
</div>

<script>
// ===== ACCORDION CORE =====
function toggleAccordion(el, group, id) {{
  var body = document.getElementById(group + '-' + id);
  var isOpen = body.classList.contains('open');
  var allBodies = document.querySelectorAll('.accordion[data-group="' + group + '"] .acc-body');
  var allHeaders = document.querySelectorAll('.accordion[data-group="' + group + '"] .acc-header');
  for (var i = 0; i < allBodies.length; i++) {{
    allBodies[i].classList.remove('open');
    var audios = allBodies[i].querySelectorAll('audio');
    for (var a = 0; a < audios.length; a++) {{
      if (!audios[a].paused) {{ audios[a].pause(); audios[a].currentTime = 0; }}
    }}
  }}
  for (var i = 0; i < allHeaders.length; i++) {{ allHeaders[i].classList.remove('open'); }}
  if (!isOpen) {{ body.classList.add('open'); el.classList.add('open'); }}
}}

// ===== ZH TOGGLE =====
function toggleZh(btn) {{
  var zh = btn.nextElementSibling;
  if (zh.style.display === 'block') {{ zh.style.display = 'none'; btn.innerHTML = '📖 顯示中文翻譯'; }}
  else {{ zh.style.display = 'block'; btn.innerHTML = '📕 隱藏中文翻譯'; }}
}}

// ===== COLLOCATION AUDIO PLAYER =====
var colloAudio = null;
function playCollo(name) {{
  if (colloAudio) {{ colloAudio.pause(); colloAudio.currentTime = 0; }}
  colloAudio = new Audio('{AP}/' + name + '.mp3');
  colloAudio.play();
}}

// ===== QUIZ =====
{quiz_js}

var quizState = [];
function renderQuiz(){{
  var c = document.getElementById('quizContainer');
  var h = '<div class="quiz-score" id="quizScore">📊 0 / ' + QUIZ.length + ' 題正確</div>';
  for(var i=0;i<QUIZ.length;i++){{
    var q = QUIZ[i];
    h += '<div class="quiz-question" id="qq' + i + '">';
    h += '<div class="quiz-q">Q' + (i+1) + '. ' + q.q + '</div>';
    h += '<div class="quiz-choices">';
    for(var j=0;j<q.choices.length;j++){{
      h += '<div class="quiz-choice" onclick="selectAnswer(' + i + ',' + j + ')" id="qc' + i + '_' + j + '">' + q.choices[j] + '</div>';
    }}
    h += '</div>';
    h += '<div class="quiz-feedback" id="qf' + i + '"></div>';
    h += '</div>';
  }}
  h += '<button class="quiz-reset" onclick="resetQuiz()">🔄 重新作答</button>';
  c.innerHTML = h;
  resetQuiz();
}}
function selectAnswer(qIdx, cIdx){{
  var q = QUIZ[qIdx];
  var fb = document.getElementById('qf' + qIdx);
  var choices = document.querySelectorAll('#qq' + qIdx + ' .quiz-choice');
  for(var i=0;i<choices.length;i++){{
    choices[i].style.pointerEvents = 'none';
    choices[i].classList.remove('selected');
    if(i === q.answer) choices[i].classList.add('correct');
    if(i === cIdx && i !== q.answer) choices[i].classList.add('wrong');
  }}
  var isCorrect = (cIdx === q.answer);
  quizState[qIdx] = isCorrect;
  fb.className = 'quiz-feedback show ' + (isCorrect ? 'correct' : 'wrong');
  fb.innerHTML = (isCorrect ? '✅ 正確！' : '❌ 答錯了。') + '<br>' + q.explain;
  updateScore();
}}
function updateScore(){{
  var correct = 0;
  for(var i=0;i<quizState.length;i++) if(quizState[i]) correct++;
  document.getElementById('quizScore').textContent = '📊 ' + correct + ' / ' + QUIZ.length + ' 題正確';
}}
function resetQuiz(){{
  quizState = [];
  for(var i=0;i<QUIZ.length;i++){{
    quizState.push(false);
    var fb = document.getElementById('qf' + i);
    if(fb){{ fb.className = 'quiz-feedback'; fb.innerHTML = ''; }}
    var choices = document.querySelectorAll('#qq' + i + ' .quiz-choice');
    for(var j=0;j<choices.length;j++){{
      if(choices[j]){{ choices[j].className = 'quiz-choice'; choices[j].style.pointerEvents = ''; }}
    }}
  }}
  updateScore();
}}
renderQuiz();
</script>
</body>
</html>'''

# Write the file
outpath = f"{BASE}/video/iguazu-falls.html"
with open(outpath, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML page generated: {outpath}")
print(f"   Size: {len(html):,} chars")

# Quick validation
checks = [
    ("20 vocab items", html.count('vocab-item') == 20),
    ("10 reading sections", html.count('data-group="reading"') == 10),
    ("8 collocation items", html.count('data-group="collo"') == 8),
    ("3 grammar items", html.count('data-group="grammar"') == 3),
    ("5 pattern items", html.count('data-group="pattern"') == 5),
    ("Vocab section in nav", 'section-vocab' in html),
    ("KK phonetics present", '/ˈsaɪləns/' in html),
    ("Parts of speech present", '動' in html and '形' in html and '名' in html),
    ("No practice remains", all(t not in html for t in ['collo-practice','grammar-practice','pattern-practice'])),
]
for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")
