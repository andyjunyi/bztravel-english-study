#!/usr/bin/env python3
"""Batch fetch YouTube transcripts for all BZ Travel videos."""
import json, sys, re, os, time

SKILL_SCRIPT = "/home/andy/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py"

# All videos except Iguazu (already done)
VIDEOS = [
    ("AOEr5FrW-lY", "We Were Almost Entirely Wrong About China", 135647, "20260603", "20:38", "culture", "中國"),
    ("Wt6zlGkLkAg", "4 Days in Italy's Best-Kept Secret: The Puglia Region", 17586, "20260429", "17:25", "nature", "義大利"),
    ("-SdS5FIRPRQ", "Bari, Matera & the Adriatic Coast Unfiltered", 4548, "20260426", "24:14", "city", "義大利"),
    ("Aoa6o2LX1qw", "Rio Before Carnival: Copacabana, Sugarloaf & Santa Teresa", 4317, "20260330", "15:28", "city", "巴西"),
    ("hIxeU4CfQTs", "48 Hours in Buenos Aires", 4141, "20260318", "16:26", "city", "阿根廷"),
    ("gK8KeV3atMs", "Mendoza Argentina: Wineries & Asado", 13600, "20260311", "13:55", "culture", "阿根廷"),
    ("hsuOrmwA8ME", "Valparaíso: Chile's Wildest, Most Colorful City", 2391, "20260308", "10:57", "city", "智利"),
    ("9ByeJ2ciOZU", "Is Santiago Worth Visiting?", 6168, "20260305", "15:02", "city", "智利"),
    ("R2FO8sojBKo", "From Lima to La Paz: A Journey with an Oxygen Tank", 1236, "20260302", "11:08", "tips", "秘魯/玻利維亞"),
    ("F09ZsBdvRtM", "Is Machu Picchu Worth the Journey?", 2534, "20260228", "8:41", "nature", "秘魯"),
    ("iFd23H04Aeo", "Peru's Sacred Valley: Better Than We Imagined!", 1535, "20260222", "12:45", "nature", "秘魯"),
    ("kZSdNRqXoMs", "Exploring LIMA Like a Local", 1179, "20260218", "12:31", "city", "秘魯"),
    ("Fd0cTlKWqfY", "10 Days in the Same Clothes! Flight & Baggage Disaster", 2270, "20260215", "13:06", "tips", "旅行"),
    ("M7UL58ZUwPg", "Bulgaria Switches to Euro: The Night Money Changed Forever", 2503, "20260105", "8:13", "culture", "保加利亞"),
    ("2XgCVknUKvI", "Our Biggest Year Yet: Planning a 2026 World Tour", 2447, "20251212", "17:45", "tips", "旅行"),
    ("vMYxjauZeF4", "3 Days in Berlin", 941, "20251201", "19:39", "city", "德國"),
    ("CIpEEV4szag", "Bernina Express & Gotthard Panorama: Alps to Lakes", 2770, "20251106", "27:15", "nature", "瑞士"),
    ("jb1RyVyIgCI", "Zermatt, Glacier Express & Matterhorn", 2150, "20251027", "15:31", "nature", "瑞士"),
    ("WTUkFRamohk", "Swiss Riviera and Panoramic Cogwheel Train to Zermatt", 1259, "20251018", "10:20", "nature", "瑞士"),
    ("BW50QKcpii4", "Interlaken's Best: Funicular, Lakes and Golden Pass Express", 1466, "20251015", "16:35", "nature", "瑞士"),
    ("3v6-o7aWXpc", "Lucerne to Interlaken: Switzerland's Panoramic Train", 2107, "20251011", "10:16", "nature", "瑞士"),
    ("kiz7SmjHVcU", "Central Kalahari Desert Safari", 1524, "20250925", "10:33", "nature", "波札那"),
    ("bqC_TPAP8L4", "We Flew Into Africa's Eden | Okavango Delta Safari", 3081, "20250917", "11:26", "nature", "波札那"),
    ("mleW-igGD2k", "Okavango Delta: Is It Overhyped?", 4000, "20250908", "16:50", "nature", "波札那"),
    ("g3ACqCX0m-w", "Is Chobe Overhyped? Real Botswana Safari", 9096, "20250901", "18:39", "nature", "波札那"),
    ("kC1OAiEQKeQ", "Victoria Falls & Zambezi Sunset Cruise", 2736, "20250828", "10:37", "nature", "辛巴威"),
    ("O09X6VVgXUA", "Ultimate Safari Adventure in Sabi Sands", 4405, "20250821", "22:24", "nature", "南非"),
    ("F_MhHEQ6MmE", "South Africa Safari Dream – Big Cats Safari", 2501, "20250814", "25:31", "nature", "南非"),
    ("kNvUJvkpLH0", "Johannesburg Before the Safari", 1160, "20250809", "6:27", "city", "南非"),
]

OUTPUT = "/mnt/e/My_Projects/bztravel-english-study/data/all_transcripts.json"
results = {}
failures = []

for i, (vid, title, views, date, dur, cat, country) in enumerate(VIDEOS):
    print(f"\n[{i+1}/{len(VIDEOS)}] {title[:40]}...")
    try:
        import subprocess
        r = subprocess.run(
            ["python3", SKILL_SCRIPT, f"https://youtube.com/watch?v={vid}",
             "--language", "en", "--text-only", "--timestamps"],
            capture_output=True, text=True, timeout=60
        )
        if r.returncode == 0 and r.stdout.strip():
            results[vid] = {
                "title": title, "views": views, "date": date,
                "duration": dur, "category": cat, "country": country,
                "transcript": r.stdout.strip()
            }
            print(f"  ✅ Transcript fetched ({len(r.stdout)} chars)")
        else:
            # Try without language filter
            r2 = subprocess.run(
                ["python3", SKILL_SCRIPT, f"https://youtube.com/watch?v={vid}",
                 "--text-only", "--timestamps"],
                capture_output=True, text=True, timeout=60
            )
            if r2.returncode == 0 and r2.stdout.strip():
                results[vid] = {
                    "title": title, "views": views, "date": date,
                    "duration": dur, "category": cat, "country": country,
                    "transcript": r2.stdout.strip()
                }
                print(f"  ✅ Transcript (auto-lang) ({len(r2.stdout)} chars)")
            else:
                results[vid] = {
                    "title": title, "views": views, "date": date,
                    "duration": dur, "category": cat, "country": country,
                    "transcript": None
                }
                failures.append(vid)
                print(f"  ❌ No transcript")
    except Exception as e:
        results[vid] = {
            "title": title, "views": views, "date": date,
            "duration": dur, "category": cat, "country": country,
            "transcript": None
        }
        failures.append(vid)
        print(f"  ❌ Error: {e}")

# Save
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n\n=== DONE ===")
print(f"Fetched: {len(results) - len(failures)}/{len(VIDEOS)}")
print(f"Failed: {len(failures)}")
for v in failures:
    print(f"  - {v}: {results.get(v, {}).get('title', '?')}")
