"""Pluggable LLM step. Turns raw section text into ADHD beat JSON.
Providers: 'manual' (no API; expects hand-written JSON), 'anthropic' (uses ANTHROPIC_API_KEY env var
only if you opt in with BEATBOOK_LLM=anthropic). Never reads keys from files."""
import json, os, urllib.request
PROMPT = """You are a patient tutor for an ADHD learner. Rewrite the source into JSON:
{"title":..., "sections":[{"title":..., "visual": one of [vectors,span,transform,compose,dice,birthday,review,network,sigmoid,kernel,gram,waves,holdout,bars,stop,flow],
 "beats":[3-7 strings, each ONE idea, 1-3 short sentences, plain words first; define jargon once like 'term (meaning)'],
 "example": one real-world example, "sayback": a Feynman 'say it back' prompt,
 "quiz":[{"q":...,"a":...}] (1-2), "tieback": optional one-line link to trading/Liquid Bot}]}
Use your own words. Never copy sentences from the source. Output JSON only.\n\nSOURCE:\n"""
class Provider:
    def generate(self, title, text): raise NotImplementedError
class Manual(Provider):
    def generate(self, title, text):
        raise SystemExit("No LLM provider enabled. Write content/<id>.json by hand, or set BEATBOOK_LLM=anthropic.")
class Anthropic(Provider):
    def generate(self, title, text):
        key = os.environ["ANTHROPIC_API_KEY"]
        body = {"model": os.environ.get("BEATBOOK_MODEL", "claude-sonnet-4-5"), "max_tokens": 8000,
                "messages": [{"role": "user", "content": PROMPT + f"TITLE: {title}\n\n" + text[:60000]}]}
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(body).encode(),
              {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
        out = json.load(urllib.request.urlopen(req, timeout=300))["content"][0]["text"]
        return json.loads(out[out.find("{"): out.rfind("}") + 1])
def get_provider():
    return {"anthropic": Anthropic}.get(os.environ.get("BEATBOOK_LLM", "manual"), Manual)()
