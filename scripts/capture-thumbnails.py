#!/usr/bin/env python3
"""Generate slide thumbnails for a deck via Playwright headless Chromium.

Usage:
    python3 _capture-thumbnails.py <deck-html> <slide-count> <out-prefix>
        deck-html    e.g. pre-boarding-vibe-coding.html
        slide-count  total number of slides (e.g. 16)
        out-prefix   filename prefix; output files: img/slides/<prefix>-NN.png

Animations are frozen via injected CSS so slides with continuous motion
do not time out.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent  # project root (one level up from scripts/)

deck = sys.argv[1] if len(sys.argv) > 1 else "pre-boarding-vibe-coding.html"
total = int(sys.argv[2]) if len(sys.argv) > 2 else 16
prefix = sys.argv[3] if len(sys.argv) > 3 else "preboarding"

deck_path = (ROOT / deck).resolve()
out_dir = ROOT / "img" / "slides"
out_dir.mkdir(parents=True, exist_ok=True)

FREEZE_CSS = """
*, *::before, *::after {
  animation-duration: 0s !important;
  animation-delay: 0s !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0s !important;
  transition-delay: 0s !important;
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
    page = context.new_page()
    page.goto(f"file://{deck_path}")
    page.add_style_tag(content=FREEZE_CSS)
    page.wait_for_selector(".slide", timeout=10000)
    page.wait_for_timeout(300)

    for i in range(total):
        # Bypass goTo() entirely: directly toggle the .active class so the
        # transition machinery does not race with animation freezing.
        page.evaluate(
            f"""
            (() => {{
              const slides = document.querySelectorAll('.slide');
              slides.forEach(s => {{
                s.classList.remove('active', 'exit-left', 'exit-right', 'fx-play');
                s.style.cssText = '';
              }});
              const target = slides[{i}];
              if (!target) return;
              target.classList.add('active', 'fx-play');
              if (typeof applyStaggerDelays === 'function') applyStaggerDelays(target);
              if (typeof playCountUps === 'function') playCountUps(target);
            }})();
            """
        )
        page.wait_for_timeout(250)
        nn = f"{i + 1:02d}"
        out_path = out_dir / f"{prefix}-{nn}.png"
        page.screenshot(path=str(out_path), full_page=False)
        print(f"  slide {nn}: {out_path.name}")

    browser.close()

print(f"done. wrote {total} thumbnails to {out_dir}/")
