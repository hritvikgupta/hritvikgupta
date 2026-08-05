#!/usr/bin/env python3
"""Render the static profile cards (hero + project cards) as light-theme SVGs.

These don't change often, so they're generated once and committed. Re-run after
editing the CARDS / HERO data below:  python3 scripts/generate_cards.py
"""

from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG, BORDER, HAIR = "#FFFFFF", "#E3E6EA", "#EDF0F3"
INK, MUTED, DIM, ACCENT = "#16191D", "#525C68", "#8B95A1", "#E14D2A"
SOFT = "#F6F8FA"
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace'
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Helvetica, Arial, sans-serif'
STYLE = f'<defs><style>.mono{{font-family:{MONO}}}.sans{{font-family:{SANS}}}</style></defs>'

CHIPS = ["AGENTS", "LLM-INFRA", "RAG", "EVALS", "CLOUD-OPS", "TERMINAL-TOOLS"]

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


def agent_loop(cx, cy, r=88, nw=94, nh=26):
    """The perception -> reasoning -> action -> verification cycle."""
    import math

    def pt(deg):
        a = math.radians(deg)
        return cx + r * math.cos(a), cy + r * math.sin(a)

    arcs = []
    for start, end in [(305, 345), (15, 55), (125, 165), (195, 235)]:
        x1, y1 = pt(start)
        x2, y2 = pt(end)
        arcs.append(f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}"/>')

    nodes = []
    for label, (nx, ny) in [
        ("PERCEPTION", (cx, cy - r)),
        ("REASONING", (cx + r, cy)),
        ("ACTION", (cx, cy + r)),
        ("VERIFICATION", (cx - r, cy)),
    ]:
        nodes.append(
            f'<rect x="{nx - nw / 2:.1f}" y="{ny - nh / 2:.1f}" width="{nw}" height="{nh}" rx="7" '
            f'fill="{SOFT}" stroke="{BORDER}"/>'
            f'<text class="mono" x="{nx:.1f}" y="{ny + 3.5:.1f}" font-size="8.5" letter-spacing="1.1" '
            f'fill="{MUTED}" text-anchor="middle">{label}</text>'
        )

    return f"""
  <g fill="none" stroke="#C6CDD5" stroke-width="1.2" marker-end="url(#arrow)">{''.join(arcs)}</g>
  <circle cx="{cx}" cy="{cy}" r="27" fill="none" stroke="#F0BCAC" stroke-width="1" stroke-dasharray="2 4"/>
  <text class="mono" x="{cx}" y="{cy + 3}" font-size="8" letter-spacing="1.5" fill="{ACCENT}" text-anchor="middle">MEMORY</text>
  {''.join(nodes)}
  <text class="mono" x="{cx}" y="{cy + r + 40}" font-size="8.5" letter-spacing="2" fill="{DIM}" text-anchor="middle">THE LOOP I OPTIMIZE</text>"""


def hero():
    chips, x = [], 44.0
    for label in CHIPS:
        w = len(label) * 6.0 + len(label) * 1.4 + 22
        chips.append(
            f'<rect x="{x:.1f}" y="288" width="{w:.1f}" height="26" rx="13" fill="{SOFT}" stroke="{BORDER}"/>'
            f'<text class="mono" x="{x + w / 2:.1f}" y="305" font-size="10" letter-spacing="1.4" '
            f'fill="{MUTED}" text-anchor="middle">{label}</text>'
        )
        x += w + 8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="400" viewBox="0 0 1280 400" role="img" aria-label="Hritvik Gupta — AI Engineer at Penn Medicine. I build agents that do real work, not demos.">
  <title>Hritvik Gupta — AI Engineer @ Penn Medicine</title>
  {STYLE}
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0.5 L9 5 L0 9.5 Z" fill="#C6CDD5"/>
    </marker>
  </defs>

  <rect x="0.5" y="0.5" width="1279" height="399" rx="16" fill="{BG}" stroke="{BORDER}"/>
  <line x1="0" y1="52.5" x2="1280" y2="52.5" stroke="{HAIR}"/>
  <line x1="0" y1="347.5" x2="1280" y2="347.5" stroke="{HAIR}"/>

  <text class="mono" x="44" y="33" font-size="11.5" letter-spacing="1.6" fill="{INK}">~/hritvik $ whoami</text>
  <text class="mono" x="1236" y="33" font-size="11" letter-spacing="1.4" fill="{DIM}" text-anchor="end">HRITVIKGUPTA.GITHUB.IO</text>

  <rect x="44" y="92" width="7" height="7" fill="{ACCENT}"/>
  <text class="mono" x="62" y="98.5" font-size="11" letter-spacing="2.4" fill="{ACCENT}">AI ENGINEER @ PENN MEDICINE · VERMA LAB</text>

  <text class="sans" x="42" y="168" font-size="62" font-weight="700" letter-spacing="-2" fill="{INK}">HRITVIK GUPTA</text>
  <rect x="44" y="188" width="72" height="2.5" fill="{ACCENT}"/>

  <text class="sans" x="44" y="232" font-size="22" font-weight="600" letter-spacing="-0.4" fill="{INK}">I build agents that do <tspan fill="{ACCENT}">real work</tspan> — not demos.</text>
  <text class="sans" x="44" y="260" font-size="14.5" fill="{MUTED}">Multi-agent orchestration · longitudinal memory · RAG &amp; retrieval ·</text>
  <text class="sans" x="44" y="279" font-size="14.5" fill="{MUTED}">eval harnesses · LLM infrastructure</text>
  {''.join(chips)}

  <text class="mono" x="44" y="378" font-size="10.5" letter-spacing="1.6" fill="{MUTED}">MS COMPUTER ENGINEERING · UC RIVERSIDE</text>
  <text class="mono" x="640" y="378" font-size="10.5" letter-spacing="1.6" fill="{DIM}" text-anchor="middle">100K+ PATIENTS SERVED</text>
  <text class="mono" x="1236" y="378" font-size="10.5" letter-spacing="1.6" fill="{DIM}" text-anchor="end">PYTHON · TYPESCRIPT · SWIFT</text>
  {agent_loop(1070, 196)}
</svg>
"""


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
    (ASSETS / "hero.svg").write_text(hero())
    for slug, idx, title, lines, foot in CARDS:
        (ASSETS / f"{slug}.svg").write_text(project_card(idx, title, lines, foot))
    print(f"wrote hero.svg and {len(CARDS)} project cards")


if __name__ == "__main__":
    main()
