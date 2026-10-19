#!/usr/bin/env bash
# One-command deploy of ADHD2Quant to Cloudflare Pages (project: adhd2quant -> adhd2quant.pages.dev)
# Needs an existing sign-in: `npx wrangler login` once, or CLOUDFLARE_API_TOKEN (+ CLOUDFLARE_ACCOUNT_ID) in env.
set -e; cd "$(dirname "$0")"
python3 build.py
npx -y wrangler pages project create adhd2quant --production-branch main 2>/dev/null || true
npx -y wrangler pages deploy dist/site --project-name adhd2quant --branch main --commit-dirty=true
