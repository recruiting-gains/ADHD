"""Import the 365-day study tracker (read-only) into schedule.json."""
import json, re, openpyxl
def import_tracker(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    titles = {}
    if "arXiv check" in wb.sheetnames:
        for r in list(wb["arXiv check"].iter_rows(values_only=True))[1:]:
            if r[0]: titles[str(r[0])] = r[1]
    days = []
    for r in list(wb["Tracker"].iter_rows(values_only=True))[1:]:
        if not r[0]: continue
        day, date, block, item, link, avl = r[:6]
        m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", str(link or "")) or re.search(r"\b(\d{4}\.\d{4,5})\b", str(item or ""))
        aid = m.group(1) if m else None
        days.append({"day": int(day), "date": date.strftime("%Y-%m-%d") if date else None, "block": block,
                     "item": item, "link": link, "arxiv_id": aid, "arxiv_title": titles.get(aid),
                     "lesson": f"day-{int(day):03d}"})
    return days
