#!/usr/bin/env python3
"""Beatbook builder.
  python3 build.py                      # rebuild site from content/ + study plan
  python3 build.py --arxiv 2609.34474   # make a new paper lesson via the LLM step (needs BEATBOOK_LLM)
  python3 build.py --file notes.txt --id my-notes --track school
"""
import argparse, json, glob, os, shutil, zipfile
from beatbook import ingest, llm, schedule
HERE = os.path.dirname(os.path.abspath(__file__))
TRACKER = "/workspace/study-plan/Liquid_Bot_Study_Tracker.xlsx"
TRACKS = {"today": "Today", "papers": "Papers", "foundations": "Foundations", "liquidbot": "Liquid Bot Lab", "school": "School"}
# weave: which extra lessons ride along with each block of the plan
WEAVE = {"1": ["f-ev-variance", "lb-expectancy"], "2": ["bis102-l13", "lb-overfitting"]}

def generate(track, lid, title, text):
    secs = ingest.split_sections(text)
    data = llm.get_provider().generate(title, "\n\n".join(f"## {t}\n{b[:8000]}" for t, b in secs))
    data.update(id=lid, track=track, subtitle=data.get("subtitle", ""))
    json.dump(data, open(f"{HERE}/content/{lid}.json", "w"), indent=1, ensure_ascii=False)

def build():
    lessons = {os.path.basename(p)[:-5]: json.load(open(p)) for p in sorted(glob.glob(f"{HERE}/content/*.json")) if not p.endswith("schedule.json")}
    days = schedule.import_tracker(TRACKER) if os.path.exists(TRACKER) else []
    for d in days:
        d["ready"] = d["lesson"] in lessons
        d["extras"] = WEAVE.get(str(d["block"] or "")[:1], ["dkh"])
    json.dump(days, open(f"{HERE}/content/schedule.json", "w"), indent=1, ensure_ascii=False, default=str)
    out = f"{HERE}/dist/site"; os.makedirs(out, exist_ok=True)
    with open(f"{out}/data.js", "w") as f:
        f.write("window.BB=" + json.dumps({"tracks": TRACKS, "lessons": lessons, "days": days}, ensure_ascii=False, default=str) + ";")
    for n in os.listdir(f"{HERE}/web"): shutil.copy(f"{HERE}/web/{n}", out)
    z = f"{HERE}/dist/adhd2quant-site.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in glob.glob(f"{out}/*"): zf.write(p, "adhd2quant/" + os.path.basename(p))
    print(f"built {len(lessons)} lessons, {len(days)} days -> {out}/index.html ; zip {z}")

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--arxiv"); a.add_argument("--file"); a.add_argument("--day", type=int)
    a.add_argument("--id"); a.add_argument("--track", default="papers"); a.add_argument("--title", default="")
    o = a.parse_args()
    if o.arxiv: generate(o.track, o.id or o.arxiv, o.title or o.arxiv, ingest.from_arxiv(o.arxiv))
    elif o.file: generate(o.track, o.id or os.path.basename(o.file).split(".")[0], o.title or o.file, ingest.from_file(o.file))
    elif o.day:  # generate a plan day from its schedule entry (paper text if it has an arXiv ID)
        d = next(x for x in schedule.import_tracker(TRACKER) if x["day"] == o.day)
        text = ingest.from_arxiv(d["arxiv_id"]) if d["arxiv_id"] else f"Teach this study item from general knowledge: {d['item']}"
        generate("today", d["lesson"], d["item"], text)
    build()
