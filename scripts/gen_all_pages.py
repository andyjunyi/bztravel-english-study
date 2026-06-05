#!/usr/bin/env python3
"""Batch generate HTML pages for all BZ Travel videos."""
import json, re

BASE = "/mnt/e/My_Projects/bztravel-english-study"
HTML_DIR = f"{BASE}/video"
DATA_FILE = f"{BASE}/data/videos.json"

with open(DATA_FILE) as f:
    videos = json.load(f)

EXISTING_PAGES = {"xW5SlCvx2W0"}
CAT_EMOJI = {"nature":"🌿","city":"🏙️","culture":"🎭","tips":"💡"}
CAT_NAMES = {"nature":"自然奇景","city":"城市探索","culture":"文化體驗","tips":"旅遊技巧"}

def make_slug(title):
    s = title.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())[:40]
    return s

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'","&#39;")

def gen_quiz_js(quiz):
    items = []
    for q in quiz:
        qtext = q.get("q") or q.get("question", "")
        choices = q.get("choices", [])
        answer = q.get("answer", 0)
        explanation = q.get("explanation") or q.get("explain", "")
        item = {
            "q": qtext,
            "choices": choices,
            "answer": answer,
            "explain": explanation
        }
        items.append(json.dumps(item, ensure_ascii=False))
    return "[" + ",".join(items) + "]"

def gen_html(v):
    vid = v["video_id"]
    title = v["title"]
    dur = v["duration"]
    country = v["country"]
    cat = v["category"]
    emoji = CAT_EMOJI.get(cat, "🌍")
    cat_name = CAT_NAMES.get(cat, "")
    
    article = v["article"]
    paras = []
    for i, (eng, chi) in enumerate(zip(article["english"], article["chinese"])):
        heading = esc(eng["heading"])
        en_text = esc(eng["text"])
        zh_text = esc(chi["text"])
        paras.append(f'''    <div class="accordion" data-group="reading">
      <div class="acc-header" onclick="toggleAccordion(this,'reading','p{i+1}')">
        <span class="acc-label">{i+1}. {heading}</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="reading-p{i+1}">
        <div class="acc-audio"><audio src="../audio/{vid}/p{i+1}.mp3" controls preload="none" onerror="this.style.display='none'"></audio></div>
        <div class="para-en">{en_text}</div>
        <button class="para-zh-toggle" onclick="toggleZh(this)">显示中文翻译</button>
        <div class="para-zh">{zh_text}</div>
      </div>
    </div>''')
    
    collos = []
    for i, c in enumerate(v["collocations"]):
        phrase = esc(c["phrase"])
        meaning = esc(c["meaning"])
        example = esc(c.get("example",""))
        practice = esc(c.get("practice",""))
        answer = esc(c.get("practice_answer",""))
        collos.append(f'''    <div class="accordion" data-group="collo">
      <div class="acc-header" onclick="toggleAccordion(this,'collo','c{i+1}')">
        <span class="acc-label">{i+1}. {phrase} <span class="collo-play" onclick="event.stopPropagation();playAudio('{vid}','collo{i+1}')">🔊</span></span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="collo-c{i+1}">
        <div class="collo-meaning">{meaning}</div>
        <div class="collo-example"><span class="label">文中例句</span><br>"{example}" <span class="collo-play-sm" onclick="playAudio('{vid}','ex{i+1}')">🔊</span></div>
        <div class="collo-practice">{practice}<br><span class="collo-answer" id="ca{i+1}">{answer}</span></div>
      </div>
    </div>''')
    
    grams = []
    for i, g in enumerate(v["grammar"]):
        point = esc(g["point"])
        explain = esc(g.get("explanation",""))
        practice = esc(g.get("practice",""))
        answer = esc(g.get("practice_answer",""))
        exs = []
        for ex in g.get("examples", []):
            ft = esc(ex.get("from_text",""))
            an = esc(ex.get("analysis","")).replace("\\n","<br>")
            pt = esc(ex.get("pattern",""))
            exs.append(f'''          <div class="ge-item">
            <div class="ge-from">{ft}</div>
            <div class="ge-analysis">{an}</div>
            <div class="ge-pattern">{pt}</div>
          </div>''')
        grams.append(f'''    <div class="accordion" data-group="grammar">
      <div class="acc-header" onclick="toggleAccordion(this,'grammar','g{i+1}')">
        <span class="acc-label">{point}</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="grammar-g{i+1}">
        <div class="grammar-explain">{explain}</div>
        <div class="grammar-examples">{"".join(exs)}</div>
        <div class="grammar-practice">{practice}<br><span class="grammar-answer" id="ga{i+1}">{answer}</span></div>
      </div>
    </div>''')
    
    pats = []
    for i, pt in enumerate(v["sentence_patterns"]):
        pattern = esc(pt["pattern"])
        meaning = esc(pt.get("meaning",""))
        example = esc(pt.get("example",""))
        template = esc(pt.get("template",""))
        drill = esc(pt.get("drill",""))
        answer = esc(pt.get("drill_answer",""))
        pats.append(f'''    <div class="accordion" data-group="pattern">
      <div class="acc-header" onclick="toggleAccordion(this,'pattern','pt{i+1}')">
        <span class="acc-label">{pattern}</span>
        <span class="acc-icon">▾</span>
      </div>
      <div class="acc-body" id="pattern-pt{i+1}">
        <div class="pattern-meaning">{meaning}</div>
        <div class="pattern-example">{example}</div>
        <div class="pattern-template">{template}</div>
        <div class="pattern-practice">{drill}<br><span class="pattern-answer" id="pa{i+1}">{answer}</span></div>
      </div>
    </div>''')
    
    collo_count = len(v["collocations"])
    gram_count = len(v["grammar"])
    pat_count = len(v["sentence_patterns"])
    quiz_count = len(v["quiz"])
    quiz_js = gen_quiz_js(v["quiz"])
    
    # JS core (minimal inline to avoid f-string conflicts)
    js_core = '''var colloAudio=null;function playAudio(vid,name){if(colloAudio){colloAudio.pause();colloAudio.currentTime=0}colloAudio=new Audio('../audio/'+vid+'/'+name+'.mp3');colloAudio.play();colloAudio.onended=function(){colloAudio=null}}
function toggleAccordion(el,group,id){var body=document.getElementById(group+'-'+id);var isOpen=body.classList.contains('open');var allBodies=document.querySelectorAll('.accordion[data-group="'+group+'"] .acc-body');var allHeaders=document.querySelectorAll('.accordion[data-group="'+group+'"] .acc-header');for(var i=0;i<allBodies.length;i++){allBodies[i].classList.remove('open');var audios=allBodies[i].querySelectorAll('audio');for(var a=0;a<audios.length;a++){if(!audios[a].paused){audios[a].pause();audios[a].currentTime=0;}}}for(var i=0;i<allHeaders.length;i++){allHeaders[i].classList.remove('open');}if(!isOpen){body.classList.add('open');el.classList.add('open');}}
function toggleZh(btn){var zh=btn.nextElementSibling;if(zh.style.display==='block'){zh.style.display='none';btn.innerHTML='📖 \\u663e\\u793a\\u4e2d\\u6587\\u7ffb\\u8bd1';}else{zh.style.display='block';btn.innerHTML='📕 \\u9690\\u85cf\\u4e2d\\u6587\\u7ffb\\u8bd1';}}'''
    
    html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>''' + title + ''' — 英文自學講義 | BZ Travel</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:#f0f4ff;color:#1e293b;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;max-width:100vw;overflow-x:hidden;line-height:1.6}
.header{background:linear-gradient(135deg,#0c4a6e,#1e40af,#3b82f6);padding:20px 16px 60px;position:relative;color:#fff;text-align:center}
.header::after{content:'';position:absolute;bottom:-1px;left:0;right:0;height:30px;background:#f0f4ff;border-radius:30px 30px 0 0}
.header-badge{display:inline-block;background:rgba(255,255,255,.15);padding:4px 14px;border-radius:20px;font-size:12px;letter-spacing:1px;margin-bottom:10px}
.header h1{font-size:20px;font-weight:700;margin-bottom:4px;line-height:1.3}
.header .sub{font-size:13px;opacity:.85}
.header-meta{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:8px;font-size:12px;opacity:.9}
.main-wrap{max-width:800px;margin:0 auto;padding:0 16px 100px}
.video-wrap{position:relative;margin-top:-40px;z-index:2;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,.15);background:#000}
.video-wrap iframe{display:block;width:100%;aspect-ratio:16/9;border:none}
.section{border-radius:16px;background:#fff;padding:20px;margin-bottom:14px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.section-title{font-size:17px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:8px}
.section-sub{font-size:12px;color:#94a3b8;margin-bottom:14px}
.accordion{border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;margin-bottom:8px}
.accordion:last-child{margin-bottom:0}
.acc-header{display:flex;align-items:center;justify-content:space-between;padding:10px 12px;cursor:pointer;background:#fafafa;transition:all .2s;user-select:none;gap:6px}
.acc-header:hover{background:#eff6ff}
.acc-header.open{background:#eff6ff;border-bottom:1px solid #e2e8f0}
.acc-label{font-size:13px;font-weight:600;flex:1;line-height:1.3}
.acc-icon{flex-shrink:0;width:20px;height:20px;border-radius:50%;background:#e2e8f0;color:#64748b;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;transition:all .3s}
.acc-header.open .acc-icon{background:#1e40af;color:#fff;transform:rotate(180deg)}
.acc-body{display:none;padding:12px;background:#fff;animation:fadeIn .2s ease}
.acc-body.open{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
.para-en{font-size:14px;line-height:1.8;color:#1e293b;margin-bottom:8px}
.para-zh-toggle{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:600;color:#3b82f6;cursor:pointer;background:#eff6ff;padding:4px 10px;border-radius:6px;border:none;margin-bottom:6px}
.para-zh{display:none;font-size:13px;color:#64748b;line-height:1.8;padding:8px 10px;background:#f8fafc;border-radius:8px;border-left:3px solid #3b82f6}
.collo-meaning{font-size:12px;color:#64748b;margin-bottom:6px}
.collo-example{font-size:12px;color:#334155;background:#f8fafc;padding:6px 8px;border-radius:6px;margin-bottom:6px;border-left:3px solid #10b981}
.collo-example .label{font-weight:600;color:#10b981;font-size:11px}
.collo-practice{font-size:12px;color:#92400e;background:#fffbeb;padding:6px 8px;border-radius:6px;border-left:3px solid #f59e0b;margin-bottom:4px}
.collo-answer{display:none;margin-top:4px;color:#059669;font-weight:600;font-size:12px}
.grammar-explain{font-size:12px;color:#64748b;margin-bottom:8px;line-height:1.6}
.grammar-examples{background:#f5f3ff;border-radius:8px;padding:8px 10px;margin-bottom:8px}
.ge-from{font-size:12px;color:#6d28d9;font-style:italic;margin-bottom:2px}
.ge-analysis{font-size:11px;color:#475569;line-height:1.5}
.ge-pattern{font-size:11px;color:#7c3aed;font-weight:600;margin-top:2px;padding:2px 6px;background:#ede9fe;border-radius:4px;display:inline-block}
.grammar-practice{font-size:12px;color:#92400e;background:#fffbeb;padding:6px 8px;border-radius:6px;border-left:3px solid #f59e0b}
.grammar-answer{display:none;margin-top:4px;color:#059669;font-weight:600}
.pattern-formula{font-size:14px;font-weight:700;color:#0891b2}
.pattern-meaning{font-size:12px;color:#64748b;margin-bottom:6px}
.pattern-example{font-size:12px;color:#334155;background:#ecfeff;padding:6px 8px;border-radius:6px;margin-bottom:6px;border-left:3px solid #06b6d4}
.pattern-template{font-size:11px;color:#0891b2;font-weight:600;background:#ecfeff;padding:3px 6px;border-radius:4px;display:inline-block;margin-bottom:6px}
.pattern-practice{font-size:12px;color:#92400e;background:#fffbeb;padding:6px 8px;border-radius:6px;border-left:3px solid #f59e0b}
.pattern-answer{display:none;margin-top:4px;color:#059669;font-weight:600}
.acc-audio audio{width:100%;height:34px;border-radius:6px;margin-bottom:6px}
.collo-play,.collo-play-sm{display:inline-flex;align-items:center;justify-content:center;cursor:pointer;transition:all .2s;border-radius:50%;flex-shrink:0}
.collo-play{width:26px;height:26px;font-size:13px;background:rgba(30,64,175,.1);vertical-align:middle;margin-left:4px}
.collo-play:active{background:#1e40af;transform:scale(.9)}
.collo-play-sm{width:22px;height:22px;font-size:11px;background:rgba(16,185,129,.1);vertical-align:middle;margin-left:3px}
.collo-play-sm:active{background:#10b981;transform:scale(.9)}
.quiz-question{border:1px solid #e2e8f0;border-radius:12px;padding:12px;margin-bottom:10px}
.quiz-q{font-size:14px;font-weight:600;margin-bottom:6px;line-height:1.4}
.quiz-choices{display:grid;gap:5px}
.quiz-choice{padding:8px 12px;border:2px solid #e2e8f0;border-radius:8px;font-size:13px;cursor:pointer;transition:all .2s;background:#fafafa}
.quiz-choice:hover{border-color:#93c5fd;background:#eff6ff}
.quiz-choice.correct{border-color:#059669;background:#d1fae5;color:#065f46}
.quiz-choice.wrong{border-color:#dc2626;background:#fef2f2;color:#991b1b}
.quiz-feedback{display:none;margin-top:8px;padding:8px 10px;border-radius:8px;font-size:12px;line-height:1.5}
.quiz-feedback.show{display:block}
.quiz-feedback.correct{background:#d1fae5;border-left:4px solid #059669;color:#065f46}
.quiz-feedback.wrong{background:#fef2f2;border-left:4px solid #dc2626;color:#991b1b}
.quiz-score{text-align:center;padding:12px;font-size:16px;font-weight:700;background:#f0f4ff;border-radius:12px;margin-bottom:10px}
.quiz-reset{display:block;width:100%;padding:10px;border:none;border-radius:8px;background:#e2e8f0;color:#475569;font-size:14px;font-weight:600;cursor:pointer}
.quiz-reset:hover{background:#cbd5e1}
.section-nav{display:flex;gap:5px;overflow-x:auto;padding:12px 0 6px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.section-nav::-webkit-scrollbar{display:none}
.section-nav a{flex-shrink:0;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;text-decoration:none;background:#e2e8f0;color:#475569;white-space:nowrap}
.section-nav a:hover,.section-nav a.active{background:#1e40af;color:#fff}
.footer{text-align:center;padding:24px 16px 16px;font-size:12px;color:#94a3b8}
.footer a{color:#3b82f6;text-decoration:none}
@media(max-width:480px){.header h1{font-size:17px}.section{padding:12px}.acc-header{padding:8px 10px}.acc-label{font-size:12px}}
</style>
</head>
<body>
<div class="header">
  <div class="header-badge">''' + emoji + ''' BZ Travel · 英文自學講義</div>
  <h1>''' + title + '''</h1>
  <div class="sub">''' + country + '''</div>
  <div class="header-meta">
    <span>''' + dur + '''</span>
    <span>''' + emoji + ''' ''' + cat_name + '''</span>
  </div>
</div>
<div class="main-wrap">
  <div class="video-wrap">
    <iframe src="https://www.youtube.com/embed/''' + vid + '''" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <div class="section-nav">
    <a href="#section-reading" class="active">📖 閱讀</a>
    <a href="#section-collocations">🔗 搭配詞</a>
    <a href="#section-grammar">📐 文法</a>
    <a href="#section-patterns">🧩 句型</a>
    <a href="#section-quiz">📝 測驗</a>
  </div>
  <div id="section-reading" class="section">
    <div class="section-title"><span>📖</span> 全文閱讀</div>
    <div class="section-sub">點選段落標題展開，其他段落自動收起</div>
''' + "\n".join(paras) + '''
  </div>
  <div id="section-collocations" class="section">
    <div class="section-title"><span>🔗</span> 實用搭配詞 <span style="font-size:12px;font-weight:400;color:#94a3b8">''' + str(collo_count) + ''' 組</span></div>
    <div class="section-sub">點選搭配詞展開完整內容</div>
''' + "\n".join(collos) + '''
  </div>
  <div id="section-grammar" class="section">
    <div class="section-title"><span>📐</span> 文法重點 <span style="font-size:12px;font-weight:400;color:#94a3b8">''' + str(gram_count) + ''' 點</span></div>
    <div class="section-sub">點選文法點展開說明</div>
''' + "\n".join(grams) + '''
  </div>
  <div id="section-patterns" class="section">
    <div class="section-title"><span>🧩</span> 關鍵句型 <span style="font-size:12px;font-weight:400;color:#94a3b8">''' + str(pat_count) + ''' 組</span></div>
    <div class="section-sub">點選句型展開範例與練習</div>
''' + "\n".join(pats) + '''
  </div>
  <div id="section-quiz" class="section">
    <div class="section-title"><span>📝</span> 閱讀測驗 <span style="font-size:12px;font-weight:400;color:#94a3b8">''' + str(quiz_count) + ''' 題</span></div>
    <div class="section-sub">點選答案即時對答</div>
    <div id="quizContainer"></div>
  </div>
  <div class="footer">
    <p>📺 來源：<a href="https://youtube.com/@bztravel" target="_blank">BZ Travel</a></p>
    <p style="margin-top:4px">Generated by Hermes Agent · 摺疊式學習</p>
  </div>
</div>
<script>
''' + js_core + '''
var QUIZ = ''' + quiz_js + ''';
var quizState = [];
function renderQuiz(){var c=document.getElementById('quizContainer');var h='<div class="quiz-score" id="quizScore">📊 0 / '+QUIZ.length+' 題正確</div>';for(var i=0;i<QUIZ.length;i++){var q=QUIZ[i];h+='<div class="quiz-question" id="qq'+i+'"><div class="quiz-q">Q'+(i+1)+'. '+q.q+'</div><div class="quiz-choices">';for(var j=0;j<q.choices.length;j++){h+='<div class="quiz-choice" onclick="selectAnswer('+i+','+j+')" id="qc'+i+'_'+j+'">'+q.choices[j]+'</div>'}h+='</div><div class="quiz-feedback" id="qf'+i+'"></div></div>'}h+='<button class="quiz-reset" onclick="resetQuiz()">🔄 重新作答</button>';c.innerHTML=h;resetQuiz()}
function selectAnswer(qIdx,cIdx){var q=QUIZ[qIdx];var fb=document.getElementById('qf'+qIdx);var choices=document.querySelectorAll('#qq'+qIdx+' .quiz-choice');for(var i=0;i<choices.length;i++){choices[i].style.pointerEvents='none';if(i===q.answer)choices[i].classList.add('correct');if(i===cIdx&&i!==q.answer)choices[i].classList.add('wrong')}var ok=(cIdx===q.answer);quizState[qIdx]=ok;fb.className='quiz-feedback show '+(ok?'correct':'wrong');fb.innerHTML=(ok?'✅ 正確！':'❌ 答錯了。')+'<br>'+q.explain;updateScore()}
function updateScore(){var c=0;for(var i=0;i<quizState.length;i++)if(quizState[i])c++;document.getElementById('quizScore').textContent='📊 '+c+' / '+QUIZ.length+' 題正確'}
function resetQuiz(){quizState=[];for(var i=0;i<QUIZ.length;i++){quizState.push(false);var fb=document.getElementById('qf'+i);if(fb){fb.className='quiz-feedback';fb.innerHTML=''}var choices=document.querySelectorAll('#qq'+i+' .quiz-choice');for(var j=0;j<choices.length;j++){if(choices[j]){choices[j].className='quiz-choice';choices[j].style.pointerEvents=''}}}}updateScore()
renderQuiz();
</script>
</body>
</html>'''
    
    slug = make_slug(title)
    fname = f"{slug}.html"
    path = f"{HTML_DIR}/{fname}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  {fname}")
    return fname, slug

# Generate all pages
pages = {}
for v in videos:
    if v["video_id"] in EXISTING_PAGES:
        continue
    fname, slug = gen_html(v)
    tags = [v["country"]]
    cat_name = CAT_NAMES.get(v["category"], "")
    if cat_name: tags.append(cat_name)
    summary = v.get("summary", "")
    if isinstance(summary, list): summary = " ".join(summary)
    pages[fname] = {
        "video_id": v["video_id"], "title": v["title"],
        "category": v["category"], "country": v["country"],
        "views": v["views"], "date": v["date"],
        "duration": v["duration"], "summary": summary, "tags": tags
    }

print(f"\n=== Generated {len(pages)} pages ===")
with open(f"{BASE}/data/pages_index.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)
print("OK")
