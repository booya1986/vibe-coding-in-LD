#!/usr/bin/env python3
"""
Generate Hebrew speaker-notes audio with ElevenLabs.

Usage:
    export ELEVENLABS_API_KEY=xi-api-...
    pip install elevenlabs
    python3 scripts/generate-audio.py

Reads narration text from speaker-notes.html (one per slide), generates
mp3 per slide via ElevenLabs Multilingual v2, and saves to audio/slide-NN.mp3.

Run from repo root.
"""
import os
import re
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = REPO_ROOT / "speaker-notes.html"
AUDIO_DIR = REPO_ROOT / "audio"

# Hebrew voice. Default: Rachel (multilingual). Override with env.
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # Sarah, multilingual; works well for Hebrew
MODEL_ID = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")

# Optional: only regenerate slides whose text changed (md5)
FORCE = os.environ.get("FORCE_REGEN", "0") == "1"


def load_eleven():
    try:
        from elevenlabs.client import ElevenLabs
    except ImportError:
        sys.stderr.write("elevenlabs package not installed. Run: pip install elevenlabs\n")
        sys.exit(1)
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        sys.stderr.write("Set ELEVENLABS_API_KEY env var.\n")
        sys.exit(1)
    return ElevenLabs(api_key=api_key)


def extract_slide_texts(html: str):
    """Extract narration text per slide from speaker-notes.html.

    Each slide is a <section class="slide" id="sNN" ...> with one or more
    <div class="section"> blocks. Inside, text comes from <p> and <li>.
    """
    out = []
    slide_pattern = re.compile(
        r'<section class="slide"\s+id="(s\d+)"\s+data-num="(\d+)"\s+data-title="([^"]*)"[^>]*>(.*?)</section>',
        re.DOTALL,
    )
    for m in slide_pattern.finditer(html):
        sid, num, title, body = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        # Find the .section block(s)
        section_pattern = re.compile(r'<div class="section[^"]*">(.*?)</div>\s*(?=</div>)', re.DOTALL)
        sections = section_pattern.findall(body)
        if not sections:
            # Fallback: just grab paragraphs
            section_text = body
        else:
            section_text = "\n".join(sections)
        # Get paragraphs and list items, skipping stage directions
        # Tag-name boundary: `<p>` or `<p ...>` only, NOT `<path>`
        nodes = re.findall(r'<(p|li)(\s[^>]*)?>(.*?)</\1>', section_text, re.DOTALL)
        lines = []
        for tag, attrs, content in nodes:
            if 'opacity:0.6' in attrs:
                continue  # skip stage direction
            text = strip_tags(content).strip()
            text = normalize_text(text)
            if text:
                lines.append(text)
        merged = " ".join(lines)
        out.append({
            "id": sid,
            "num": num,
            "title": title,
            "text": merged,
        })
    out.sort(key=lambda s: s["num"])
    return out


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_text(s: str) -> str:
    # Replace fancy quotes with plain ones for clearer TTS
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    # Spell out symbols that TTS misreads
    s = s.replace("&", "ו")
    return s


def text_hash(text: str) -> str:
    import hashlib
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:10]


def main():
    if not HTML_PATH.exists():
        sys.exit(f"Not found: {HTML_PATH}")
    AUDIO_DIR.mkdir(exist_ok=True)
    html = HTML_PATH.read_text(encoding="utf-8")
    slides = extract_slide_texts(html)
    if not slides:
        sys.exit("No slides parsed.")
    print(f"Parsed {len(slides)} slides.")

    eleven = load_eleven()

    manifest = []
    for s in slides:
        num = s["num"]
        out_path = AUDIO_DIR / f"slide-{num:02d}.mp3"
        hash_path = AUDIO_DIR / f"slide-{num:02d}.hash"
        new_hash = text_hash(s["text"])
        old_hash = hash_path.read_text().strip() if hash_path.exists() else ""

        if not FORCE and out_path.exists() and old_hash == new_hash:
            print(f"  skip slide-{num:02d} (cached, {out_path.stat().st_size//1024}KB)")
            manifest.append({"num": num, "title": s["title"], "file": out_path.name, "duration": None})
            continue

        print(f"  gen  slide-{num:02d} ({len(s['text'])} chars) ...", flush=True)
        try:
            audio_iter = eleven.text_to_speech.convert(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                text=s["text"],
                output_format="mp3_44100_128",
            )
            with open(out_path, "wb") as f:
                for chunk in audio_iter:
                    if chunk:
                        f.write(chunk)
            hash_path.write_text(new_hash)
            print(f"     -> {out_path.name} ({out_path.stat().st_size//1024}KB)")
            manifest.append({"num": num, "title": s["title"], "file": out_path.name})
            time.sleep(0.4)  # gentle rate limit
        except Exception as e:
            sys.stderr.write(f"  FAIL slide-{num:02d}: {e}\n")
            sys.exit(1)

    # Write manifest for the HTML to load
    import json
    manifest_path = AUDIO_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {manifest_path.relative_to(REPO_ROOT)}")
    print(f"Total: {len(manifest)} files in {AUDIO_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
