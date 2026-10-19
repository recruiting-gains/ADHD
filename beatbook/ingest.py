"""Get text from an arXiv ID, a PDF, or a text file; split into rough sections."""
import re, subprocess, urllib.request, tempfile, os
def from_arxiv(aid):
    p = os.path.join(tempfile.gettempdir(), f"bb_{aid}.pdf")
    if not os.path.exists(p): urllib.request.urlretrieve(f"https://arxiv.org/pdf/{aid}", p)
    return from_pdf(p)
def from_pdf(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
def from_file(path):
    return from_pdf(path) if path.lower().endswith(".pdf") else open(path, encoding="utf-8", errors="ignore").read()
HEAD = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Z][^\n]{2,80})$", re.M)
def split_sections(text, max_sections=8):
    hits = [m for m in HEAD.finditer(text) if "." not in m.group(1)]
    if len(hits) < 2: # fallback: equal chunks
        n = max(1, len(text) // 6000); step = len(text) // n
        return [(f"Part {i+1}", text[i*step:(i+1)*step]) for i in range(n)][:max_sections]
    out = [(m.group(2).strip(), text[m.end(): (hits[i+1].start() if i+1 < len(hits) else len(text))]) for i, m in enumerate(hits)]
    return out[:max_sections]
