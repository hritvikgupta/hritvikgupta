#!/usr/bin/env python3
"""Render the project cards as GitHub-dark SVGs.

These don't change often, so they're generated once and committed. Re-run after
editing the CARDS / HERO data below:  python3 scripts/generate_cards.py
"""

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from font import STACK, face_css  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# GitHub dark palette, so the cards sit inside the page instead of on top of it
BG, BORDER, HAIR = "#0d1117", "#30363d", "#21262d"
INK, MUTED, DIM, ACCENT = "#e6edf3", "#8b949e", "#6e7681", "#FF6B4A"
SOFT = "#161b22"
STYLE = f'<defs><style>{face_css()}.mono,.sans{{font-family:{STACK}}}</style></defs>'

CARDS = [
    ("card-nimbus", "01", "nimbus",
     ["An AI cloud control plane — one agent that reads your code and",
      "acts on real AWS & GCP credentials to fix your infra."],
     "AWS · GCP · SELF-HOSTED · BSL-1.1"),
    ("card-reagent", "02", "reagent",
     ["Autonomous research agents that read the literature, weigh the",
      "evidence, and return a cited, reproducible answer."],
     "TYPESCRIPT · MULTI-AGENT · MIT"),
    ("card-archimyst", "03", "Archimyst Terminal",
     ["A council of agents in your terminal — symbol indexing and",
      "coordinated edits across million-line codebases."],
     "PYTHON · CLI · MIT"),
    ("card-tine", "04", "Tine",
     ["A second cursor that watches your screen, suggests help, and —",
      "on your say-so — takes over and finishes the task."],
     "SWIFT 6 · MACOS 13+ · MENU BAR"),
]


def project_card(idx, title, lines, foot):
    alt = f"{title} — {lines[0]} {lines[1]}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="520" height="196" viewBox="0 0 520 196" role="img" aria-label="{escape(alt)}">
  <title>{escape(alt)}</title>
  {STYLE}
  <rect x="0.5" y="0.5" width="519" height="195" rx="13" fill="{BG}" stroke="{BORDER}"/>
  <text class="mono" x="26" y="40" font-size="11" letter-spacing="1.8" fill="{ACCENT}">{idx}</text>
  <text class="sans" x="26" y="82" font-size="24" font-weight="600" letter-spacing="-0.5" fill="{INK}">{escape(title)}</text>
  <text class="sans" x="26" y="110" font-size="12.5" fill="{MUTED}">{escape(lines[0])}</text>
  <text class="sans" x="26" y="130" font-size="12.5" fill="{MUTED}">{escape(lines[1])}</text>
  <line x1="26" y1="152.5" x2="494" y2="152.5" stroke="{HAIR}"/>
  <text class="mono" x="26" y="175" font-size="9.5" letter-spacing="1.5" fill="{DIM}">{escape(foot)}</text>
  <text class="sans" x="494" y="176" font-size="13" fill="{DIM}" text-anchor="end">&#8599;</text>
</svg>
"""


def main():
    ASSETS.mkdir(exist_ok=True)
    for slug, idx, title, lines, foot in CARDS:
        (ASSETS / f"{slug}.svg").write_text(project_card(idx, title, lines, foot))
    print(f"wrote {len(CARDS)} project cards")


if __name__ == "__main__":
    main()
