# ADHD2Quant

An ADHD-friendly, 365-day AI / quant study app (PWA). Four tracks, short lessons, quizzes.

Live: https://adhd2quant.pages.dev

## Build
```
python build.py
```
Output goes to `dist/`. Lesson content lives in `content/` and `content_src.py`; the web app is in `web/`.

Optional AI content generation: set `BEATBOOK_LLM=anthropic` and `ANTHROPIC_API_KEY` in your environment (never commit keys).

## Deploy
Cloudflare Pages, project `adhd2quant`: zip the built site so files sit at the zip root, then use Direct Upload in the Cloudflare dashboard. (`deploy.sh` does the same via wrangler.)
