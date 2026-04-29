# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Two deliverables, both single-file HTML, no build step, no framework, no package manager:

1. **`index.html`** — the **presentation deck** ("Vibe Coding in L&D") delivered at the Amdocs Meetup, branded for Bank Hapoalim's L&D division. CSS, JS, slide HTML all live in one file. Media assets in `img/`, `vid/`, `sound/`.
2. **`speaker-notes.html`** — the **speaker-prep companion**: mobile-first one-slide-per-page reference with thumbnail (from `img/slides/slide-NN.png`), expanded narration, single continuous audio playback (`audio/narration.mp3`), TOC drawer, and bottom nav. Navigation is decoupled from audio: scrolling between slides does NOT pause/restart playback.

The repo is published as a **public GitHub repo** at `booya1986/vibe-coding-in-LD` with GitHub Pages enabled at `https://booya1986.github.io/vibe-coding-in-LD/`. Both deliverables ship from `main` branch root.

## How to "run" / preview

```bash
open index.html              # the deck (default browser)
open speaker-notes.html      # the speaker companion
```

That is the entire dev loop. Any edit → save → reload the browser tab. Pushing to `main` auto-deploys to GitHub Pages within ~30-60 seconds.

## Critical conventions (these are non-negotiable rules the user has set)

These are baked-in rules that have been hardened over many iterations. **Treat all of them as project invariants.** When in doubt, do not introduce a violation — even if a single edit looks fine, the whole deck must stay consistent.

### Text content rules

1. **No em-dashes (—) or en-dashes (–) anywhere in user-facing text.** Replace with `,`, `:`, parentheses, or split into separate phrases.
2. **No middle dots (`·`) between Hebrew words.** The `·` is allowed *only* inside `<span class="slide-label">` (the small red tag at the top of each slide). Anywhere else (bullets, body, headings, card titles), use a comma, colon, or just a space.
3. **No emojis in headings, slide titles, card titles, or buttons.** Always use SVG outline icons (`stroke-width: 1.4–1.6`, `fill: none`, `stroke-linecap: round`, `stroke-linejoin: round`) inside a red-tinted square container (`background: rgba(255,32,32,0.12)`, `border-radius: 7-8px`). Emojis are tolerable only in `.md-summary` style decorative summary lines.
4. **Hard line breaks belong in CSS, not in copy.** Don't insert `<br>` to fix wrapping — adjust `font-size`, `max-width`, or `white-space` instead.

### Heading & color rules

5. **Main headings (`h1.slide-title`, `h2.slide-heading`) are white only.** Do not wrap any portion in `<span style="color:var(--accent)">`. Red is reserved for: `slide-label`, `accent-line`, neon-stress on body text/strong tags, decorative backgrounds, hero numbers, links, and animated elements.
6. **The cover/title slide title uses `white-space: nowrap`** to keep the headline on one line. Other slide headings may wrap.
7. **Slide-label is the only place red `·` separators are allowed.** It's the small uppercase red tag at the top of each slide.

### RTL & alignment rules

8. **Strict RTL throughout.** `<html dir="rtl">`. Every card / list / panel needs `direction: rtl; text-align: right;`. Even mockups inside `<iframe>`-style frames (browser, terminal, LMS) must be RTL.
9. **Icon-first cards: `flex-direction: row` (NOT `row-reverse`) with `direction: rtl`.** This places the icon on the right edge, glued next to the title (the natural Hebrew reading order). Using `row-reverse` looks correct visually but breaks accessibility and breaks again when nested.
10. **Card titles always sit beside their icon on the right side** — never floating in a corner, never centered, never separated by a wide gap.
11. **Navigation arrow direction is the RTL trap.** `prev-btn` (right side) shows `›` (right-pointing chevron); `next-btn` (left side) shows `‹` (left-pointing chevron). Both buttons need `direction: ltr; unicode-bidi: isolate;` so the RTL document doesn't flip the chevron itself. The keyboard mapping is the inverse: `→` = prev, `←` = next.

### Bullet & list rules

12. **Bullets with title + description go stacked, not inline.** Use `.bullet-list.bullet-stacked` with `<span class="b-title">` + `<span class="b-desc">`. The bullet dot is `position: absolute; right: 0;` so it stays anchored to the right edge regardless of title length. Inline bullets with `<strong>foo:</strong> bar` are only acceptable for short, single-line items.

### Logo, layout & sizing rules

13. **Logo path is `img/לוגו.png` with `filter: brightness(0) invert(1);`** to render it white. Default `height: 83px` (it lives in `.logo-wrap`). Same logo appears on the title slide and the CTA slide.
14. **Default workhorse layout is `split` with text on the right and the visual on the left.** When the user asks for "more space for the visual", weight via `flex: 1.3` / `flex: 1.4` on the visual column rather than inline `max-width`.
15. **When the user asks for relative resizing ("20% bigger", "make it half"), apply the change consistently to all related properties** — `max-width`, `font-size` (clamp values), `padding`, `gap`. Don't scale only one and leave others.
16. **Match font sizes to the rest of the deck.** New components inherit the typography scale — body text `clamp(0.78rem, 1.15vw, 0.9rem)`, card titles `clamp(0.85rem, 1.2vw, 1rem)`, descriptions `clamp(0.7rem, 1vw, 0.85rem)`. Don't introduce arbitrary `font-size: 12px`.

## Design system (already defined in the file — reuse, don't redesign)

CSS custom properties at the top of `<style>`:

| Token | Value | Use |
|---|---|---|
| `--bg` | `#111111` | dark background |
| `--accent` | `#FF2020` | neon red (primary) |
| `--accent-light` | `#FF6060` | brighter red |
| `--accent-glow` / `--accent-glow2` | red rgba layers | for `text-shadow` / `box-shadow` neon effects |
| `--text-1/2/3` | white → light gray → mid gray | typography hierarchy |
| `--border` / `--border-h` | subtle / red hover | card borders |

Font: **Heebo** (300–800) loaded from Google Fonts.

Body has a faint red grid background pattern. Each `.slide` has an additional `radial-gradient` red glow.

## Slide architecture

Every slide is `<div class="slide" data-layout="...">` inside `#slide-container`. Layouts (case-sensitive `data-layout` value):

- `title` — cover. Logo (`img/לוגו.png`, `height: 83px`) centered bottom.
- `centered` — single hero/break statement.
- `split` — text right, visual left (the workhorse layout). Tune `flex` to weight columns.
- `divider` — section opener. Big translucent text behind (`USE CASE`, `01`, etc.).
- `quote` — source statistic with `<mark>` highlights, source label as `slide-label`, link button at the bottom.
- `cta` — final slide with QR placeholder (black background, neon-red outline) + logo.
- `guru`, `team`, `process`, `content`, `cards`, `cards2`, `agenda`, `timeline`, `demo`, `video`, `about` — also exist; reuse rather than introduce new ones.

Reusable components (all CSS already exists — read the file before adding new classes):

- `.browser-frame` (Mac-style window, used for video, dashboards, mockups, exam UI)
- `.exam-section` (numbered phase card with title + bullets)
- `.bullet-list.bullet-stacked` (title-on-top, desc-below bullets)
- `.highlight-box` (red-bordered call-out, RTL)
- `.tri-card` (glassmorphism with `blue|purple|green` accent stripe)
- `.mock-wa` / `.mock-cal` / `.mock-mail` (animated WhatsApp / calendar / email mockups)
- `.tc-resp-card`, `.tc-mini` (responsibility cards)
- `.md-card` (SKILL.md document mock with file tab + YAML body + Hebrew summary)
- `.day-stat` / `.pyramid-stat` / `.funnel-hero` (stat blocks)
- `.process-flow` / `.pipeline` / `.timeline` / `.trinity-circles` / `.hitl-stage` / `.cmd-stage` / `.pyramid-stage` / `.funnel-stage` (full diagrams)
- `.comp-table` with `.c-30 ... .c-90` cell classes (heatmap red→yellow→green)
- `.retro-dashboard` (3 colored zones for retrospective)

## Navigation contract (already implemented in `<script>`)

- **Right-side button + `→` + `PageUp` + `Backspace`** → `goPrev()` (in RTL, right = backwards).
- **Left-side button + `←` + `Space` + `PageDown` + `Enter`** → `goNext()`.
- Touch swipe with 60px threshold.
- Dot indicators (active dot widens and shows the slide number).
- Top progress bar (`#progress-bar`) animates with red gradient.
- `#kbd-hint` bottom-right shows `← → Space` keys faintly.

Disable `prev` on slide 0, `next` on last slide.

## Media handling (the rule that has bitten before)

If a slide contains `<video>` or sound:

- A `userHasInteracted` flag is set on the first document `click` so autoplay-with-sound is allowed afterwards (browsers block autoplay with audio without user gesture).
- On entering the video slide: `slideVideo.currentTime = 0; slideVideo.play().catch(() => {})`.
- **On leaving** (in `goTo()`, BEFORE the 520ms animation timeout — at the very top of the function): `slideVideo.pause()` + `currentTime = 0`. Audio bleeding into the next slide is the bug to avoid; pausing inside the `setTimeout` callback runs too late.
- The same pattern is wired for `guruSound` (`sound/sound3.mp3`) — pause immediately when leaving the guru slide. Any new sound effect needs the same hook.
- Save `prevIndex` to a variable BEFORE `current = index` so `handleVideoSlide(newIndex, prevIndex)` gets the correct comparison.

## Visual idioms (use established ones, don't invent new ones)

For concept-heavy slides, pair the right-side text with one of these existing visuals on the left:

- **Connected nodes** (השילוש הקדוש style): SVG circles at corners + animated dashed `tc-arrow-path` arcs.
- **Pyramid / hierarchy**: SVG `<path>` polygons with `linearGradient` red→transparent, glow filter, icons aligned to each tier with dashed connector lines.
- **Insight funnel**: top dot cloud (CSS repeating `radial-gradient`) → hero number → SVG funnel with brain icon → animated bar chart.
- **Process flow**: 4 cells in a row with the last (`pf-highlight`) at `flex: 1.6` with red border, inner glow, and a different content tone.
- **HITL / Cycle**: center hub circle + 3 satellite circles + animated arrows between them.
- **Heatmap table**: `.comp-table` with cell classes `c-30 ... c-90` for color gradient (red → yellow → green).
- **Retro dashboard**: 3 stacked colored zones (green / yellow / red) with badge + number + icon row.
- **Floating particles** (`.cc-pf`) for hero scenes with code/data context.

When the user describes a new diagram, first scan whether one of these idioms fits before designing from scratch.

## Animations (already defined, use them)

Existing keyframes near each component's CSS:

- `cc-typing-bounce` — bounce on mascot/character images
- `arrow-flow` — dashed line flowing along an SVG path
- `ring-pulse` — neon glow pulse on circles
- `bubble-in` — chat bubble entry
- `progress-shimmer` — progress bar pulsing
- `bar-rise` — bars rising into place
- `cc-pf-drift` — floating decorative particles
- `cal-pulse` / `banner-shine` / `selected-pulse` / `timer-blink` / `cc-blink`

**Stagger `animation-delay`** so elements enter in sequence (0.3s, 1.5s, 2.7s — not all at once).

## File / asset paths

- Hebrew filenames are used liberally (`img/לוגו.png`, `img/גורו.png`, `img/אבי לוי.png`, `img/מיילר.heic` → converted to `img/mailer.jpg`).
- **HEIC → JPG conversion** (the user often drops `.heic` from iPhone Photos):
  ```bash
  sips -s format jpeg "img/<name>.heic" --out "img/<slug>.jpg" --resampleWidth 600
  ```
  Also resample large PNGs (Gemini-generated images can be 2048×2048) to ~800px width to keep the deck snappy.
- **PNG with white background → transparent**: convert via Python Pillow (replace near-white pixels with alpha 0). Mix-blend-mode CSS doesn't fully erase white on a near-black page.
- Reference image asset: `img/dashboard.png` (BI dashboard screenshot inside the browser frame on the day-of-execution slide).
- Mascot image (Claude Code): `img/mascot.png`.
- **`img/slides/slide-01.png` … `slide-26.png`** — 1600×900 thumbnails of every slide, used by `speaker-notes.html`. Regenerate via Playwright by loading `index.html`, calling `goTo(N)`, and screenshotting; freeze animations with a CSS override before capturing or `slide-15` (funnel) and `slide-17` will time out from continuous animations.
- **`audio/narration.mp3`** — continuous Hebrew narration produced by ElevenLabs `eleven_multilingual_v2` + voice `cgSgspJ2msm6clMCkdW9` ("Jessica" preset), with `VoiceSettings(stability=0.35, similarity_boost=0.75, style=0.55, speed=1.1, use_speaker_boost=True)` for a snappier, more rhythmic delivery (the speaker explicitly asked for "יותר קצבי"). Concatenated from per-slide MP3s with `ffmpeg -f concat`. Only `narration.mp3` ships in git; per-slide chunks and `*.hash` cache files are gitignored. The cache key now includes voice id + model + settings, so changing `ELEVENLABS_VOICE_ID` / `VOICE_SPEED` / etc. auto-invalidates all cached chunks and re-renders.
- **`GMT20260428-071117_Recording.m4a`** — internal Zoom rehearsal audio. **Always gitignored** (private). Whisper transcript at `/tmp/whisper-out/rehearsal.txt` is also private.

## Workflow when the user asks for changes

The user iterates fast and gives short feedback. Patterns I've learned:

- **"תגדיל ב-20%"** → multiply ALL related properties (max-width, font-size base + clamp values, padding, gap, icon size). Not just one.
- **"זה לא מיושר לימין"** → the issue is almost always `flex-direction: row-reverse` instead of `row` with `direction: rtl`. Switch and verify.
- **"תוריד את האימוג'י"** → replace with an SVG outline icon in a red-tinted square container. Match the existing icon library style (1.4–1.6 stroke).
- **"תוריד את ה-em-dash"** → audit the entire file for `—` and `–`, not just the line they pointed at. Same with `·` (middle dot) outside `slide-label`.
- **"שנה לבן"** → the user means: remove every red color reference inside this heading. That includes `<span>`, inline `style="color:..."`, and `text-shadow` on the inner span.
- **Asset dropped in folder** → check `img/` listing, convert HEIC if needed, update the `<img src="...">` path. Don't assume the filename — list the directory.
- **"תעלה למעלה" / "במרכז" / "למטה"** → adjust the slide's `justify-content` and `padding-top/-bottom` rather than introducing margins on inner elements.
- **"תוסיף שקף"** → insert before `<!-- CTA / Summary -->`. After adding, verify the dot-nav still aligns and the keyboard hint remains visible.
- **Consistency over locality**: if the user changes one card, apply the same change to peer cards in the same slide and to similar cards in sibling slides where it makes sense.

## Project-scoped skill

`.claude/skills/poalim-presentation/SKILL.md` is a project-local Claude Code skill that documents this design system and reusable components. Read it before redesigning any slide — it is the canonical reference for: design tokens, hard rules (no em-dashes, no emojis, white-only headings), all standard layouts, the full component catalogue, animation keyframes, and the navigation contract. Treat it as the spec; treat the index.html as the implementation.

## Speaker prep companion (speaker-notes.html)

Independent file, served from same Pages root. Mobile-first, designed for the speaker to prep on phone before the meetup.

### Structure
- 26 `<section class="slide" id="sNN" data-num="N" data-title="...">` blocks, each is `100vh` with `scroll-snap-align: start`.
- Per slide: tag (top right), slide number, title, accent line, duration pill, thumbnail (`img/slides/slide-NN.png`), single `<div class="section">` containing only the **קריינות** (narration). All meta sections (mood/tone/anecdote/avoid) were removed by user request, only the actual script remains.
- TOC drawer slides in from the left (RTL: `left: -100%; .open → left: 0`). Wrapped by `<aside class="toc">` and `<div class="toc-back">` overlay.
- Bottom nav: TOC toggle, prev (›), title + slide-num, **Play button**, next (‹). RTL keyboard mapping is identical to `index.html`.

### Audio playback (decoupled from navigation)
- One global `Audio` element loads `audio/narration.mp3`. Single play button toggles play/pause.
- Slide navigation (swipe, arrow keys, prev/next, TOC click) does **NOT** affect audio. Audio does NOT auto-advance slides. This decoupling is intentional and was the user's explicit request.
- While playing, the play button shows elapsed time (`m:ss`) instead of a play icon.
- `tts-status` line in the TOC drawer reflects load state (HEAD request to `audio/narration.mp3`).

### Regenerating the audio
1. Edit narration text inside `<div class="section">` blocks of `speaker-notes.html` (paragraphs and `<li>` items only; stage directions in `style="opacity:0.6"` paragraphs are skipped).
2. Run:
   ```bash
   ELEVENLABS_API_KEY=xi-api-... python3 scripts/generate-audio.py
   ```
   The script uses `eleven_multilingual_v2` model + voice `cgSgspJ2msm6clMCkdW9` ("Jessica" preset) with rhythmic `VoiceSettings` (stability 0.35, style 0.55, speed 1.1). Hash-cached including voice/settings: changing the voice or speed auto-re-renders everything; otherwise only slides whose text changed are re-rendered.
3. Concatenate per-slide MP3s into the single narration file:
   ```bash
   cd audio
   { for n in $(seq -f "%02g" 1 26); do echo "file 'slide-${n}.mp3'"; done } > concat-list.txt
   ffmpeg -y -f concat -safe 0 -i concat-list.txt -c copy narration.mp3
   rm concat-list.txt
   ```
4. Commit `audio/narration.mp3`. Per-slide files and `*.hash` are gitignored.

The parser regex in `generate-audio.py` is `<(p|li)(\s[^>]*)?>(.*?)</\1>`. **Do not** change to `<(p|li)([^>]*)>` — that matches `<path>` SVG tags too, leaking SVG content into the narration.

### Rehearsal-derived content (`rehearsal-extracts.md`)
A curated extract from the Whisper transcript, organized per slide. Filtered to only substantive speaker content (no team chitchat / "wait, redo this" / Whisper noise). Use it as source-of-truth for what was said in rehearsal when revising the narration. Numbers from rehearsal worth verifying before the talk: questions count (rehearsal: 75 vs deck: 120+), respondents (1,250 vs ambiguous 1,068), 80% LLM accuracy.

## Repo & deployment

- **Git repo**: initialized with `gitignore`-ed sensitive items (rehearsal `.m4a`, transcripts, `.heic` source images, `__pycache__`, `.pdf-export/`, per-slide audio chunks, hash cache).
- **Remote**: `https://github.com/booya1986/vibe-coding-in-LD` (public, owned by `booya1986`).
- **GitHub Pages**: enabled on `main` branch, `/` path. Public URL `https://booya1986.github.io/vibe-coding-in-LD/`. Pages rebuild takes ~30-60s after `git push`. Verify with `gh api /repos/booya1986/vibe-coding-in-LD/pages` (look for `"status":"built"`).
- **Public-facing URLs**:
  - Deck: `https://booya1986.github.io/vibe-coding-in-LD/index.html`
  - Speaker companion: `https://booya1986.github.io/vibe-coding-in-LD/speaker-notes.html`
  - Audio: `https://booya1986.github.io/vibe-coding-in-LD/audio/narration.mp3`
- **Sensitive content**: the deck and speaker notes contain bank-internal anecdotes, dollar amounts ($100), and process detail. The user accepted this for a public repo because the talk is being delivered publicly.

## When making changes

- **Read the existing file before adding CSS.** The stylesheet is large (≈80+ component classes) and almost everything you need already exists.
- For visuals (diagrams, infographics): prefer SVG with the existing Gaussian blur filters (`id="oneon"`, `id="hitlGlow"`, `id="pyrGlow"`, `id="cmdGlow"`, `id="lglow"`, `id="neon"`) and the established red gradient defs. Don't introduce new color palettes.
- Animations are CSS keyframes near the relevant component. Use staggered `animation-delay` so elements enter in sequence (not all at once).
- For SVG icons inside circles: use `<g transform="translate(-X,-Y)">` to center 16×16 icons over a `<circle cx="0" cy="0">` — verify the icon visually centers, don't trust the math alone.

## Pre-deploy QA checklist

After any structural change, run through this list mentally before declaring the work done:

- [ ] Click through every slide in the browser — no overlap, no clipped content, no horizontal scrollbar.
- [ ] Progress bar reaches 100% on the final slide.
- [ ] Every `<video>` / `<audio>` pauses immediately when leaving its slide (no audio bleed).
- [ ] `grep -nE "—|–" index.html` returns 0 user-facing matches.
- [ ] Middle dots `·` exist only inside `<span class="slide-label">`.
- [ ] No emojis in any `<h1>`, `<h2>`, or `<button>`.
- [ ] `<h1 class="slide-title">` and `<h2 class="slide-heading">` contain no inner `<span>` with red color.
- [ ] All cards (`*-card`, `*-section`) have `direction: rtl; text-align: right;`.
- [ ] Keyboard navigation works: `→`/`←` and `Space`.
- [ ] Logo on cover and CTA renders white and is `height: 83px`.
- [ ] If new media files added: paths exist in `img/` / `vid/` / `sound/`.

## Reference library

- **`.claude/skills/poalim-presentation/SKILL.md`** — the canonical spec for this design system. Project-scoped (NOT global). Read it before any non-trivial redesign.
- This `CLAUDE.md` documents the project rules; the SKILL.md documents the reusable design system that can be applied to future Hapoalim presentations.
- **`speaker-notes.html`** — speaker-prep companion (see "Speaker prep companion" section above). When asked to update narration, edit only the `<p>` / `<li>` content inside `<div class="section">` blocks; do not re-introduce per-slide play buttons or other section variants (`tip` / `warn` / `bad`) — they were explicitly removed.
- **`rehearsal-extracts.md`** — curated phrases from the rehearsal transcript, organized per slide. Use as source when revising narration.
- **`scripts/generate-audio.py`** — ElevenLabs TTS generator. Uses `eleven_multilingual_v2` + Jessica preset voice with rhythmic VoiceSettings (speed 1.1, lower stability for variation). Hash-cached including voice/settings; changing any of those re-renders everything.
