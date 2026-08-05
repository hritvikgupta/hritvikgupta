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
from datetime import datetime, timezone
from html import escape
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "hritvikgupta")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# light design system
BG, BORDER, HAIR = "#FFFFFF", "#E3E6EA", "#EDF0F3"
INK, MUTED, DIM, ACCENT = "#16191D", "#525C68", "#8B95A1", "#E14D2A"
TINT = "#FBD9CE"
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
    by_year = []
    for year in range(created.year, now.year + 1):
        frm = max(created, datetime(year, 1, 1, tzinfo=timezone.utc))
        to = min(now, datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        if frm >= to:
            continue
        c = graphql(YEAR_Q, {"login": USER, "from": frm.isoformat(), "to": to.isoformat()})
        c = c["user"]["contributionsCollection"]
        year_commits = c["totalCommitContributions"] + c["restrictedContributionsCount"]
        by_year.append((year, year_commits))
        commits += year_commits
        reviews += c["totalPullRequestReviewContributions"]
        contributions += (c["contributionCalendar"]["totalContributions"]
                          + c["restrictedContributionsCount"])

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

    return {
        "name": base["name"] or base["login"],
        "created": created,
        "stars": sum(r["stargazerCount"] for r in repos),
        "forks": sum(r["forkCount"] for r in repos),
        "repos": base["repositories"]["totalCount"],
        "followers": base["followers"]["totalCount"],
        "prs": base["pullRequests"]["totalCount"],
        "issues": base["issues"]["totalCount"],
        "contributed": base["repositoriesContributedTo"]["totalCount"],
        "commits": commits,
        "by_year": by_year,
        "reviews": reviews,
        "contributions": contributions,
        "langs": langs,
    }



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
    rows = [
        ("Total stars earned", human(s["stars"])),
        ("Total commits", human(s["commits"])),
        ("Total contributions", human(s["contributions"])),
        ("Total pull requests", human(s["prs"])),
        ("Total issues", human(s["issues"])),
        ("Repositories", human(s["repos"])),
    ]
    lines = "".join(
        f'<text class="sans" x="30" y="{92 + i * 26}" font-size="13" fill="{MUTED}">{escape(label)}</text>'
        f'<text class="mono" x="300" y="{92 + i * 26}" font-size="13.5" font-weight="600" '
        f'fill="{INK}" text-anchor="end">{value}</text>'
        for i, (label, value) in enumerate(rows)
    )

    # commits per year — real, verifiable, and it actually shows a trajectory
    years = s["by_year"]
    peak = max((c for _, c in years), default=1) or 1
    x0, x1, base, tall = 342.0, 490.0, 208.0, 96.0
    bw = (x1 - x0 - (len(years) - 1) * 5) / max(len(years), 1)
    bars = []
    for i, (year, count) in enumerate(years):
        h = max(2.0, tall * count / peak)
        x = x0 + i * (bw + 5)
        bars.append(
            f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2.5" '
            f'fill="{ACCENT if count == peak else TINT}"/>'
        )
        if count == peak:
            bars.append(
                f'<text class="mono" x="{x + bw / 2:.1f}" y="{base - h - 7:.1f}" font-size="9" '
                f'font-weight="600" fill="{ACCENT}" text-anchor="middle">{count}</text>'
            )

    axis = ""
    if years:
        axis = (
            f'<text class="mono" x="{x0:.1f}" y="{base + 15}" font-size="8.5" fill="{DIM}">{years[0][0]}</text>'
            f'<text class="mono" x="{x1:.1f}" y="{base + 15}" font-size="8.5" fill="{DIM}" '
            f'text-anchor="end">{years[-1][0]}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="520" height="270" viewBox="0 0 520 270" role="img" aria-label="GitHub statistics for {USER}">
  <title>GitHub statistics — {human(s['stars'])} stars, {human(s['commits'])} commits</title>
  <defs><style>.mono{{font-family:{MONO}}}.sans{{font-family:{SANS}}}</style></defs>
  {head(520, 'GITHUB STATS', f'{datetime.now(timezone.utc).year - s["created"].year} YEARS ON GITHUB').format(h=269)}
  {lines}
  <text class="mono" x="342" y="86" font-size="9" letter-spacing="1.6" fill="{DIM}">COMMITS BY YEAR</text>
  <line x1="342" y1="{base + 0.5}" x2="490" y2="{base + 0.5}" stroke="{HAIR}"/>
  {''.join(bars)}
  {axis}
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
  <text class="mono" x="30" y="258" font-size="9" letter-spacing="1.5" fill="{DIM}">ACROSS {s['repos']} REPOSITORIES</text>
</svg>
"""



def main():
    s = fetch()
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "stats.svg").write_text(stats_card(s))
    (ASSETS / "langs.svg").write_text(langs_card(s))
    print(f"stars={s['stars']} commits={s['commits']} contributions={s['contributions']} "
          f"prs={s['prs']} issues={s['issues']} repos={s['repos']} followers={s['followers']} "
          f"by_year={s['by_year']}")


if __name__ == "__main__":
    main()
