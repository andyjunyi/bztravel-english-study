#!/usr/bin/env python3
"""Generate audio files for top BZ Travel videos."""
import json, os, subprocess, concurrent.futures, sys

BASE = "/mnt/e/My_Projects/bztravel-english-study"
DATA_FILE = f"{BASE}/data/videos.json"
AUDIO_DIR = f"{BASE}/audio"
SKIP_VIDS = {"xW5SlCvx2W0"}  # Iguazu already done

with open(DATA_FILE) as f:
    videos = json.load(f)

# Top videos by views (excluding Iguazu)
tops = sorted([v for v in videos if v["video_id"] not in SKIP_VIDS],
              key=lambda v: v["views"], reverse=True)[:10]

def gen_audio(vid, text, name):
    """Generate one audio file. Returns (name, success)."""
    vdir = f"{AUDIO_DIR}/{vid}"
    os.makedirs(vdir, exist_ok=True)
    outpath = f"{vdir}/{name}.mp3"
    if os.path.exists(outpath) and os.path.getsize(outpath) > 1000:
        return (name, True)  # already exists
    try:
        r = subprocess.run(
            ["edge-tts", "--voice", "en-US-JennyNeural",
             "--text", text[:5000], "--write-media", outpath],
            capture_output=True, text=True, timeout=60
        )
        if r.returncode == 0 and os.path.getsize(outpath) > 100:
            return (name, True)
        else:
            print(f"  ❌ {name}: {r.stderr[:100]}")
            return (name, False)
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        return (name, False)

total_files = 0
for v in tops:
    vid = v["video_id"]
    title = v["title"][:40]
    en_texts = [p["text"] for p in v["article"]["english"]]
    collo_phrases = [c["phrase"] for c in v["collocations"]]
    collo_examples = [c.get("example","") for c in v["collocations"]]
    
    # Paragraphs + full
    jobs = []
    for i, txt in enumerate(en_texts):
        jobs.append((vid, txt, f"p{i+1}"))
    full_text = " ".join(en_texts)
    jobs.append((vid, full_text, "full"))
    
    # Collocations 
    for i, ph in enumerate(collo_phrases):
        jobs.append((vid, ph, f"collo{i+1}"))
    for i, ex in enumerate(collo_examples):
        if ex:
            jobs.append((vid, ex, f"ex{i+1}"))
    
    total_this = len(jobs)
    total_files += total_this
    print(f"\n📹 {title} — {total_this} audio files")
    
    # Generate in parallel (4 at a time)
    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(gen_audio, *j): j[2] for j in jobs}
        for future in concurrent.futures.as_completed(futures):
            name, ok = future.result()
            done += 1
            if ok:
                sys.stdout.write(f"  ✅ {name}  ({done}/{total_this})\r")
            sys.stdout.flush()
    print(f"\n  ✅ {vid} done!")

print(f"\n\n=== ALL DONE ===")
print(f"Total audio files: {total_files}")
