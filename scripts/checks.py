#!/usr/bin/env python3
"""Resume quality gates. Exit 0 = all pass, 1 = has BLOCK, 2 = has FLAG only.

Usage:
    python3 checks.py resume.md [--jd jd.md] [--evidence evidence.md] [--links] [--max-pages 2]

Gates:
  1. length      — estimated page count <= max-pages
  2. quant       — share of bullet lines containing a number >= 55%
  3. ai-flavor   — zero hits against the AI-flavor wordlist (incl. em-dash)
  4. jd-coverage — keywords listed in the JD file's `关键词:` lines covered >= 70%
  5. links       — every http(s) URL in the resume answers < 400 (needs --links)
"""
import argparse
import re
import sys
import urllib.request

# Words that signal machine-generated filler. Case-insensitive for latin.
AI_FLAVOR = [
    # zh
    "赋能", "深耕", "助力", "抓手", "沉淀", "打通", "打造", "拥抱变化", "极致",
    "卓越", "精益求精", "砥砺", "波澜壮阔", "生态位", "价值转化", "全方位",
    "多维度", "行业领先", "顶尖水平", "深度洞察力", "综上所述", "总而言之",
    # en
    "spearheaded", "leveraged", "passionate about", "synergy", "results-driven",
    "dynamic professional", "seasoned expert", "honed", "delve", "meticulous",
    "proven track record", "cutting-edge", "state-of-the-art", "esteemed",
    "robust", "seamless",
]
EM_DASHES = ["——", "—", "–"]

CN_CHARS_PER_PAGE = 1150   # dense single-column zh resume
EN_WORDS_PER_PAGE = 520


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_md(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#*_>`|]", "", text)
    return text


def gate_length(text, max_pages):
    plain = strip_md(text)
    cn = len(re.findall(r"[一-鿿]", plain))
    words = len(re.findall(r"[A-Za-z]{2,}", plain))
    pages = max(cn / CN_CHARS_PER_PAGE, words / EN_WORDS_PER_PAGE)
    ok = pages <= max_pages + 0.15
    return ok, f"est {pages:.2f} pages (cn_chars={cn}, en_words={words}, limit={max_pages})"


def gate_quant(text):
    bullets = [l for l in text.splitlines() if re.match(r"\s*[-*•]\s+\S", l)]
    if not bullets:
        return False, "no bullet lines found"
    with_num = [l for l in bullets if re.search(r"\d", l)]
    ratio = len(with_num) / len(bullets)
    return ratio >= 0.55, f"{len(with_num)}/{len(bullets)} bullets quantified ({ratio:.0%}, need >=55%)"


def gate_ai_flavor(text):
    low = text.lower()
    hits = [w for w in AI_FLAVOR if w.lower() in low]
    hits += [d for d in EM_DASHES if d in text]
    return not hits, ("clean" if not hits else "hits: " + ", ".join(hits))


def gate_jd_coverage(resume_text, jd_text):
    kws = []
    for line in jd_text.splitlines():
        m = re.match(r"\s*(?:关键词|keywords)\s*[:：]\s*(.+)", line, re.I)
        if m:
            kws += [k.strip() for k in re.split(r"[,，、;/]", m.group(1)) if k.strip()]
    if not kws:
        return None, "JD file has no `关键词:` line, skipped"
    low = resume_text.lower()
    missing = [k for k in kws if k.lower() not in low]
    ratio = 1 - len(missing) / len(kws)
    msg = f"{ratio:.0%} of {len(kws)} keywords covered"
    if missing:
        msg += "; missing: " + ", ".join(missing)
    return ratio >= 0.70, msg


def gate_links(text):
    urls = sorted(set(re.findall(r"https?://[^\s)\]>」）,，]+", text)))
    if not urls:
        return None, "no links found, skipped"
    bad = []
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            code = urllib.request.urlopen(req, timeout=15).getcode()
            if code >= 400:
                bad.append(f"{u} -> {code}")
        except Exception as e:
            bad.append(f"{u} -> {type(e).__name__}")
    return not bad, ("all reachable: " + ", ".join(urls)) if not bad else "; ".join(bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume")
    ap.add_argument("--jd")
    ap.add_argument("--evidence")
    ap.add_argument("--links", action="store_true")
    ap.add_argument("--max-pages", type=float, default=2)
    args = ap.parse_args()

    resume = read(args.resume)
    results = {
        "length": gate_length(resume, args.max_pages),
        "quant": gate_quant(resume),
        "ai-flavor": gate_ai_flavor(resume),
    }
    if args.jd:
        results["jd-coverage"] = gate_jd_coverage(resume, read(args.jd))
    if args.links:
        results["links"] = gate_links(resume)
    if args.evidence:
        # Numbers in the resume must appear in evidence — advisory listing only,
        # the authoritative check is the human/agent fact pass.
        ev = read(args.evidence)
        nums = set(re.findall(r"\d[\d,.]*[%万亿kKMB+]?", strip_md(resume)))
        missing = [n for n in nums if len(n) > 1 and n not in ev]
        results["evidence-numbers"] = (None, f"{len(missing)} numbers not literally in evidence (advisory): "
                                       + ", ".join(sorted(missing)[:15]))

    block = False
    for name, (ok, msg) in results.items():
        tag = "PASS" if ok else ("SKIP" if ok is None else "BLOCK")
        if ok is False:
            block = True
        print(f"[{tag}] {name}: {msg}")
    sys.exit(1 if block else 0)


if __name__ == "__main__":
    main()
