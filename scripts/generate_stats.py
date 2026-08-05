#!/usr/bin/env python3
"""Generate the GitHub stat cards for the profile README.

Pulls real numbers from the GitHub GraphQL API and renders three SVG cards
(assets/stats.svg, assets/langs.svg, assets/contributions.svg) in the profile's
light design system. Run by .github/workflows/stats.yml on a schedule so the
cards stay current without depending on any third-party service.

Usage:  GITHUB_TOKEN=... python3 scripts/generate_stats.py
"""

import json
import math
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "hritvikgupta")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# light design system
BG, BORDER, HAIR = "#FFFFFF", "#E3E6EA", "#EDF0F3"
INK, MUTED, DIM, ACCENT = "#16191D", "#525C68", "#8B95A1", "#E14D2A"
HEAT = ["#F0F2F4", "#FBD9CE", "#F7AE97", "#EF7E5D", "#E14D2A"]
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace'
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Helvetica, Arial, sans-serif'


def graphql(query, variables):
    if not TOKEN:
        sys.exit("GITHUB_TOKEN is required")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": f"{USER}-profile-stats",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        sys.exit(f"GraphQL error: {payload['errors']}")
    return payload["data"]


PROFILE_Q = """
query($login: String!, $after: String) {
  user(login: $login) {
    name login createdAt
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, ISSUE, REPOSITORY]) { totalCount }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        name stargazerCount forkCount
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

YEAR_Q = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestReviewContributions
      contributionCalendar { totalContributions }
    }
  }
}
"""

CALENDAR_Q = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""


def fetch():
    repos, after, base = [], None, None
    while True:
        data = graphql(PROFILE_Q, {"login": USER, "after": after})["user"]
        base = base or data
        page = data["repositories"]
        repos.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    created = datetime.fromisoformat(base["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    commits = reviews = contributions = 0
    for year in range(created.year, now.year + 1):
        frm = max(created, datetime(year, 1, 1, tzinfo=timezone.utc))
        to = min(now, datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        if frm >= to:
            continue
        c = graphql(YEAR_Q, {"login": USER, "from": frm.isoformat(), "to": to.isoformat()})
        c = c["user"]["contributionsCollection"]
        commits += c["totalCommitContributions"] + c["restrictedContributionsCount"]
        reviews += c["totalPullRequestReviewContributions"]
        contributions += c["contributionCalendar"]["totalContributions"]

    cal = graphql(CALENDAR_Q, {
        "login": USER,
        "from": (now - timedelta(days=364)).isoformat(),
        "to": now.isoformat(),
    })["user"]["contributionsCollection"]["contributionCalendar"]

    # Normalise language bytes *within* each repo before summing, so a single
    # asset-heavy repository can't claim 90% of the profile.
    langs = {}
    for repo in repos:
        edges = repo["languages"]["edges"]
        repo_total = sum(e["size"] for e in edges)
        if not repo_total:
            continue
        for edge in edges:
            node = edge["node"]
            entry = langs.setdefault(node["name"], {"size": 0.0, "color": node["color"] or "#8B95A1"})
            entry["size"] += edge["size"] / repo_total

    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    current = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            current += 1
        elif current or d is not days[-1]:
            break

    return {
        "name": base["name"] or base["login"],
        "streak_current": current,
        "streak_longest": longest,
        "created": created,
        "stars": sum(r["stargazerCount"] for r in repos),
        "forks": sum(r["forkCount"] for r in repos),
        "repos": base["repositories"]["totalCount"],
        "followers": base["followers"]["totalCount"],
        "prs": base["pullRequests"]["totalCount"],
        "issues": base["issues"]["totalCount"],
        "contributed": base["repositoriesContributedTo"]["totalCount"],
        "commits": commits,
        "reviews": reviews,
        "contributions": contributions,
        "calendar": cal,
        "langs": langs,
    }


def rank(s):
    """The github-readme-stats grading curve, implemented locally."""
    def cdf(x):
        return 1 - 2 ** -x

    weights = [
        (s["commits"], 1000, 2),
        (s["contributed"], 25, 1),
        (s["issues"], 25, 1),
        (s["stars"], 50, 4),
        (s["prs"], 50, 2),
        (s["followers"], 10, 1),
        (s["reviews"], 2, 1),
    ]
    total = sum(w for _, _, w in weights)
    score = sum(cdf(value / median) * w for value, median, w in weights) / total
    percentile = (1 - score) * 100
    for grade, threshold in [("S", 1), ("A+", 12.5), ("A", 25), ("A-", 37.5),
                             ("B+", 50), ("B", 62.5), ("B-", 75), ("C+", 87.5)]:
        if percentile <= threshold:
            return grade, percentile
    return "C", percentile


def human(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1_000:
        return f"{n:,}"
    return str(n)


def arc(cx, cy, r, frac):
    """Path for a circular arc starting at 12 o'clock, sweeping clockwise."""
    frac = min(max(frac, 0.001), 0.999)
    angle = 2 * math.pi * frac - math.pi / 2
    x, y = cx + r * math.cos(angle), cy + r * math.sin(angle)
    large = 1 if frac > 0.5 else 0
    return f"M {cx} {cy - r} A {r} {r} 0 {large} 1 {x:.2f} {y:.2f}"


def head(width, label, right=""):
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{{h}}" rx="13" fill="{BG}" stroke="{BORDER}"/>'
        f'<text class="mono" x="30" y="38" font-size="11" letter-spacing="2.4" fill="{ACCENT}">{label}</text>'
        f'<text class="mono" x="{width - 30}" y="38" font-size="10" letter-spacing="1.4" fill="{DIM}" '
        f'text-anchor="end">{right}</text>'
        f'<line x1="30" y1="56.5" x2="{width - 30}" y2="56.5" stroke="{HAIR}"/>'
    )


def stats_card(s):
    grade, percentile = rank(s)
    filled = max(0.06, 1 - percentile / 100)
    years = datetime.now(timezone.utc).year - s["created"].year

    rows = [
        ("Total stars earned", human(s["stars"])),
        ("Total commits", human(s["commits"])),
        ("Total contributions", human(s["contributions"])),
        ("Total pull requests", human(s["prs"])),
        ("Total issues", human(s["issues"])),
        ("Public repositories", human(s["repos"])),
    ]
    lines = "".join(
        f'<text class="sans" x="30" y="{92 + i * 26}" font-size="13" fill="{MUTED}">{escape(label)}</text>'
        f'<text class="mono" x="330" y="{92 + i * 26}" font-size="13.5" font-weight="600" '
        f'fill="{INK}" text-anchor="end">{value}</text>'
        for i, (label, value) in enumerate(rows)
    )

    cx, cy, r = 424, 128, 44
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="520" height="270" viewBox="0 0 520 270" role="img" aria-label="GitHub statistics for {USER}">
  <title>GitHub statistics — {human(s['stars'])} stars, {human(s['commits'])} commits, rank {grade}</title>
  <defs><style>.mono{{font-family:{MONO}}}.sans{{font-family:{SANS}}}</style></defs>
  {head(520, 'GITHUB STATS', f'{years} YEARS ON GITHUB').format(h=269)}
  {lines}
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{HAIR}" stroke-width="7"/>
  <path d="{arc(cx, cy, r, filled)}" fill="none" stroke="{ACCENT}" stroke-width="7" stroke-linecap="round"/>
  <text class="sans" x="{cx}" y="{cy + 4}" font-size="27" font-weight="700" fill="{INK}" text-anchor="middle">{grade}</text>
  <text class="mono" x="{cx}" y="{cy + 22}" font-size="8" letter-spacing="1.2" fill="{DIM}" text-anchor="middle">TOP {percentile:.1f}%</text>
  <text class="mono" x="{cx}" y="{cy + 68}" font-size="8.5" letter-spacing="1.6" fill="{DIM}" text-anchor="middle">RANK</text>
</svg>
"""


def langs_card(s):
    top = sorted(s["langs"].items(), key=lambda kv: kv[1]["size"], reverse=True)[:8]
    total = sum(v["size"] for _, v in top) or 1

    bar, x = [], 30.0
    width = 400.0
    for _, meta in top:
        w = width * meta["size"] / total
        bar.append(f'<rect x="{x:.2f}" y="76" width="{max(w - 1.5, 1):.2f}" height="10" rx="3" fill="{meta["color"]}"/>')
        x += w

    legend = []
    for i, (name, meta) in enumerate(top):
        lx, ly = 30 + (i % 2) * 208, 124 + (i // 2) * 27
        pct = 100 * meta["size"] / total
        legend.append(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{meta["color"]}"/>'
            f'<text class="sans" x="{lx + 18}" y="{ly}" font-size="12.5" fill="{MUTED}">{escape(name)}</text>'
            f'<text class="mono" x="{lx + 186}" y="{ly}" font-size="11.5" fill="{DIM}" text-anchor="end">{pct:.1f}%</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="460" height="270" viewBox="0 0 460 270" role="img" aria-label="Most used languages for {USER}">
  <title>Most used languages — {', '.join(n for n, _ in top[:4])}</title>
  <defs><style>.mono{{font-family:{MONO}}}.sans{{font-family:{SANS}}}</style></defs>
  {head(460, 'MOST USED LANGUAGES', 'REPO-WEIGHTED').format(h=269)}
  {''.join(bar)}
  {''.join(legend)}
  <line x1="30" y1="240.5" x2="430" y2="240.5" stroke="{HAIR}"/>
  <text class="mono" x="30" y="258" font-size="9" letter-spacing="1.5" fill="{DIM}">ACROSS {s['repos']} PUBLIC REPOSITORIES</text>
</svg>
"""


def contributions_card(s):
    weeks = s["calendar"]["weeks"]
    total = s["calendar"]["totalContributions"]
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=0)

    def level(n):
        if n == 0:
            return HEAT[0]
        for i, cut in enumerate([0.15, 0.35, 0.6], start=1):
            if n <= max(1, peak * cut):
                return HEAT[i]
        return HEAT[4]

    cell, gap, x0, y0 = 13.0, 3.6, 62.0, 92.0
    step = cell + gap
    squares, months, seen = [], [], set()
    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            d = datetime.fromisoformat(day["date"])
            x = x0 + wi * step
            y = y0 + day["weekday"] * step
            squares.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="3" '
                f'fill="{level(day["contributionCount"])}"/>'
            )
            if d.day <= 7 and d.strftime("%b") not in seen and wi > 0:
                seen.add(d.strftime("%b"))
                months.append(
                    f'<text class="mono" x="{x:.1f}" y="{y0 - 12}" font-size="9.5" '
                    f'letter-spacing="1" fill="{DIM}">{d.strftime("%b").upper()}</text>'
                )

    days = "".join(
        f'<text class="mono" x="48" y="{y0 + i * step + 10:.1f}" font-size="9" fill="{DIM}" '
        f'text-anchor="end">{lbl}</text>'
        for i, lbl in [(1, "MON"), (3, "WED"), (5, "FRI")]
    )
    legend_x = x0 + len(weeks) * step - 130
    legend = "".join(
        f'<rect x="{legend_x + 34 + i * 17}" y="{y0 + 7 * step + 12}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>'
        for i, c in enumerate(HEAT)
    )

    width = int(x0 + len(weeks) * step + 46)
    height = int(y0 + 7 * step + 62)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{total} contributions in the last year">
  <title>{total} contributions in the last year</title>
  <defs><style>.mono{{font-family:{MONO}}}.sans{{font-family:{SANS}}}</style></defs>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="13" fill="{BG}" stroke="{BORDER}"/>
  <text class="mono" x="30" y="38" font-size="11" letter-spacing="2.4" fill="{ACCENT}">CONTRIBUTION ACTIVITY</text>
  <text class="mono" x="{width - 30}" y="38" font-size="10" letter-spacing="1.4" fill="{DIM}" text-anchor="end">{total:,} IN THE LAST YEAR · PEAK {peak}/DAY</text>
  <line x1="30" y1="56.5" x2="{width - 30}" y2="56.5" stroke="{HAIR}"/>
  {''.join(months)}
  {days}
  {''.join(squares)}
  <text class="mono" x="30" y="{y0 + 7 * step + 22}" font-size="9.5" letter-spacing="1.4" fill="{MUTED}">CURRENT STREAK <tspan fill="{ACCENT}" font-weight="600">{s['streak_current']}D</tspan>   ·   LONGEST STREAK <tspan fill="{ACCENT}" font-weight="600">{s['streak_longest']}D</tspan>   ·   PEAK <tspan fill="{ACCENT}" font-weight="600">{peak}</tspan> IN A DAY</text>
  <text class="mono" x="{legend_x}" y="{y0 + 7 * step + 22}" font-size="9" letter-spacing="1.2" fill="{DIM}">LESS</text>
  {legend}
  <text class="mono" x="{legend_x + 124}" y="{y0 + 7 * step + 22}" font-size="9" letter-spacing="1.2" fill="{DIM}">MORE</text>
</svg>
"""


def main():
    s = fetch()
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "stats.svg").write_text(stats_card(s))
    (ASSETS / "langs.svg").write_text(langs_card(s))
    (ASSETS / "contributions.svg").write_text(contributions_card(s))
    grade, percentile = rank(s)
    print(f"stars={s['stars']} commits={s['commits']} contributions={s['contributions']} "
          f"prs={s['prs']} issues={s['issues']} repos={s['repos']} followers={s['followers']} "
          f"reviews={s['reviews']} rank={grade} ({percentile:.2f}%) "
          f"lastYear={s['calendar']['totalContributions']} "
          f"streak={s['streak_current']}/{s['streak_longest']}")


if __name__ == "__main__":
    main()
