#!/usr/bin/env python3
"""
Regenerate paragraph + full audio with cleaned text.
Replaces embedded newlines with spaces so edge-tts flows naturally.
"""
import json, os, subprocess, concurrent.futures, re, sys

BASE = "/mnt/e/My_Projects/bztravel-english-study"
DATA_FILE = f"{BASE}/data/videos.json"
AUDIO_DIR = f"{BASE}/audio"

def clean_text(text: str) -> str:
    """Remove embedded newlines and normalize whitespace."""
    text = text.replace("\n", " ")
    text = re.sub(r" +", " ", text)
    return text.strip()

def gen_audio(vid, text, name):
    vdir = f"{AUDIO_DIR}/{vid}"
    os.makedirs(vdir, exist_ok=True)
    outpath = f"{vdir}/{name}.mp3"
    
    text = clean_text(text)[:5000]
    if not text:
        return (name, False, "empty text")
    
    try:
        r = subprocess.run(
            ["edge-tts", "--voice", "en-US-JennyNeural",
             "--text", text, "--write-media", outpath],
            capture_output=True, text=True, timeout=60
        )
        if r.returncode == 0 and os.path.getsize(outpath) > 100:
            return (name, True, "")
        else:
            return (name, False, r.stderr[:100])
    except Exception as e:
        return (name, False, str(e))

def process_video(v):
    vid = v["video_id"]
    title = v["title"][:40]
    en_texts = [p["text"] for p in v["article"]["english"]]
    
    jobs = []
    # Paragraphs
    for i, txt in enumerate(en_texts):
        jobs.append((vid, txt, f"p{i+1}"))
    # Full text (join paragraphs with space)
    full = " ".join(en_texts)
    jobs.append((vid, full, "full"))
    
    total = len(jobs)
    print(f"\n📹 {title} — {total} files")
    
    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(gen_audio, *j): j[2] for j in jobs}
        for f in concurrent.futures.as_completed(futures):
            name, ok, err = f.result()
            done += 1
            status = "✅" if ok else f"❌ {err}"
            sys.stdout.write(f"  {status} {name} ({done}/{total})\r")
            sys.stdout.flush()
    print()

def main():
    with open(DATA_FILE) as f:
        videos = json.load(f)
    
    print(f"Processing {len(videos)} videos...")
    for v in videos:
        process_video(v)
    
    print("\n=== ALL DONE ===")

if __name__ == "__main__":
    main()
