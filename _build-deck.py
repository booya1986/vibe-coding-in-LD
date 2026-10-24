#!/usr/bin/env python3
"""Assemble pre-boarding-vibe-coding.html from index.html skeleton + new slides."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / "index.html").read_text(encoding="utf-8")
new_slides = (ROOT / "_new-slides.html").read_text(encoding="utf-8")

m_open = re.search(r'<div id="slide-container">\s*\n', src)
m_close = re.search(r'\n  </div>\s*\n  <!-- /slide-container -->', src)
assert m_open and m_close, "could not find slide-container boundaries"

header = src[: m_open.end()]
footer = src[m_close.start() :]

footer = footer.replace("const VIDEO_SLIDE = 1;", "const VIDEO_SLIDE = -1;")
footer = footer.replace("const GURU_SLIDE = 2;", "const GURU_SLIDE = -1;")
footer = footer.replace(
    "const BONUS_SLIDES = [total - 2, total - 1]; // Free Skill + PRD Template, both fire confetti",
    "const BONUS_SLIDES = [total - 1]; // CTA fires confetti",
)

new_titles = [
    "פתיחה",
    "תחשבו על השבוע הראשון",
    "הימים הראשונים מעצבים הכל",
    "מה הארגון נותן היום",
    "Pre-Boarding",
    "14 ימים שבין חתימה להתחלה",
    "Vibe Coding",
    "אז בניתי לה דף אישי",
    "מי אנחנו, הצוות שלך",
    "מה תעשי כאן",
    "מה מחכה לך בימים הראשונים",
    "ערוץ ישיר אליי",
    "איך אני הייתי רוצה שיקבלו אותי?",
    "שלוש מסקנות",
    "לא הכל ורוד",
    "תודה",
]
titles_repr = "[\n" + ",\n".join(f"      '{t}'" for t in new_titles) + "\n    ]"
footer = re.sub(
    r"const SLIDE_TITLES = \[[^\]]*\];",
    f"const SLIDE_TITLES = {titles_repr};",
    footer,
    count=1,
    flags=re.DOTALL,
)
footer = re.sub(
    r"const TRANSITION_DUR = \{[^}]*\};",
    "const TRANSITION_DUR = {};",
    footer,
    count=1,
    flags=re.DOTALL,
)
header = re.sub(
    r"<title>[^<]*</title>",
    "<title>Pre-Boarding בעזרת Vibe Coding</title>",
    header,
    count=1,
)

# Inject per-deck CSS overrides just before </style>
# Bigger readable text + orphan prevention
OVERRIDES = """
    /* ── Pre-Boarding deck overrides ───────────────────────────── */
    /* Bigger projection-readable text */
    .bullet-stacked .b-title {
      font-size: clamp(1.02rem, 1.55vw, 1.18rem) !important;
      line-height: 1.35 !important;
    }
    .bullet-stacked .b-desc {
      font-size: clamp(0.88rem, 1.28vw, 1.0rem) !important;
      line-height: 1.55 !important;
    }
    .split-col > .slide-sub {
      font-size: clamp(0.96rem, 1.4vw, 1.08rem) !important;
    }
    /* Orphan prevention */
    h1.slide-title, h2.slide-heading {
      text-wrap: balance;
    }
    .slide-sub {
      text-wrap: balance;
    }
    .bullet-stacked .b-title, .bullet-stacked .b-desc {
      text-wrap: pretty;
    }
    /* Ensure CTA centers properly */
    .slide[data-layout="cta"] img {
      display: block;
      margin: 0 auto;
    }
"""
out = header + new_slides + footer
out = out.replace("</style>\n</head>", OVERRIDES + "  </style>\n</head>", 1)
(ROOT / "pre-boarding-vibe-coding.html").write_text(out, encoding="utf-8")
print(f"wrote pre-boarding-vibe-coding.html ({len(out):,} chars, {out.count(chr(10)):,} lines)")
slide_count = len(re.findall(r'<div class="slide(?: active)?" data-layout=', out))
print(f"slide instances: {slide_count} (expect 16)")
