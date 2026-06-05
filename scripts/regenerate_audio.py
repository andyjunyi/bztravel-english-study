#!/usr/bin/env python3
"""Regenerate paragraph audio files from transcript text for top videos."""
import json, os, subprocess, concurrent.futures

BASE = "/mnt/e/My_Projects/bztravel-english-study"
DATA_FILE = f"{BASE}/data/videos.json"
AUDIO_DIR = f"{BASE}/audio"

with open(DATA_FILE) as f:
    videos = json.load(f)

# Top 10 by views + Iguazu
targets = ["AOEr5FrW-lY", "Wt6zlGkLkAg", "gK8KeV3atMs", "g3ACqCX0m-w",
           "9ByeJ2ciOZU", "-SdS5FIRPRQ", "O09X6VVgXUA", "Aoa6o2LX1qw",
           "hIxeU4CfQTs", "mleW-igGD2k", "xW5SlCvx2W0"]

def gen_audio(vid, text, name):
    vdir = f"{AUDIO_DIR}/{vid}"
    os.makedirs(vdir, exist_ok=True)
    outpath = f"{vdir}/{name}.mp3"
    text = text[:5000]
    try:
        subprocess.run(["edge-tts", "--voice", "en-US-JennyNeural",
                       "--text", text, "--write-media", outpath],
                      capture_output=True, timeout=60)
        size = os.path.getsize(outpath) if os.path.exists(outpath) else 0
        return (name, size > 100)
    except:
        return (name, False)

for v in videos:
    if v["video_id"] not in targets:
        continue
    vid = v["video_id"]
    en_texts = [p["text"] for p in v["article"]["english"]]
    
    print(f"\n📹 {v['title'][:40]}")
    jobs = [(vid, t, f"p{i+1}") for i, t in enumerate(en_texts)]
    jobs.append((vid, " ".join(en_texts), "full"))
    
    done = 0
    total = len(jobs)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        fs = {ex.submit(gen_audio, *j): j[2] for j in jobs}
        for f in concurrent.futures.as_completed(fs):
            name, ok = f.result()
            done += 1
            print(f"  {'✅' if ok else '❌'} {name} ({done}/{total})")

print("\n=== ALL DONE ===")
