#!/usr/bin/env python3
"""Regenerate the GitHub statistics section of README.md as native markdown.

No images. Everything this writes is markdown GitHub renders itself — a Mermaid
`xychart` and plain tables — dropped in between the <!-- stats:start --> and
<!-- stats:end --> markers in README.md.

On private contributions
------------------------
GitHub does not expose them over the API: `restrictedContributionsCount` comes
back as 0 and the calendar counts public activity only, even when the request
is authenticated as the account owner. The single switch that changes this is
Settings -> Public profile -> "Include private contributions on my profile".
Turn it on and every number below counts private work too, unchanged code.

Usage:  GITHUB_TOKEN=... python3 scripts/generate_stats.py
"""

import json
import os
import re
import sys
import urllib.request
from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "hritvikgupta")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- stats:start -->", "<!-- stats:end -->"



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
    createdAt
    followers { totalCount }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""

CALENDAR_Q = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
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

    days, total, restricted = {}, 0, 0
    for year in range(created.year, now.year + 1):
        frm = max(created, datetime(year, 1, 1, tzinfo=timezone.utc))
        to = min(now, datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        if frm >= to:
            continue
        c = graphql(CALENDAR_Q, {
            "login": USER, "from": frm.isoformat(), "to": to.isoformat(),
        })["user"]["contributionsCollection"]
        total += c["contributionCalendar"]["totalContributions"]
        restricted += c["restrictedContributionsCount"]
        for week in c["contributionCalendar"]["weeks"]:
            for d in week["contributionDays"]:
                days[d["date"]] = d["contributionCount"]

    # Language share is normalised within each repo first, so one asset-heavy
    # repository can't claim most of the profile.
    langs = {}
    for repo in repos:
        edges = repo["languages"]["edges"]
        repo_total = sum(e["size"] for e in edges)
        if not repo_total:
            continue
        for edge in edges:
            langs[edge["node"]["name"]] = langs.get(edge["node"]["name"], 0.0) + edge["size"] / repo_total

    return {
        "created": created,
        "total": total + restricted,
        "restricted": restricted,
        "days": days,
        "stars": sum(r["stargazerCount"] for r in repos),
        "repos": base["repositories"]["totalCount"],
        "followers": base["followers"]["totalCount"],
        "langs": langs,
    }


def streaks(days):
    if not days:
        return (0, None, None), (0, None, None)
    ordered = sorted(days)
    first, last = date.fromisoformat(ordered[0]), date.fromisoformat(ordered[-1])

    best, run_len, run_start = (0, None, None), 0, None
    day = first
    while day <= last:
        if days.get(day.isoformat(), 0) > 0:
            run_start = run_start or day
            run_len += 1
            if run_len > best[0]:
                best = (run_len, run_start, day)
        else:
            run_len, run_start = 0, None
        day += timedelta(days=1)

    cur_len, cur_end = 0, None
    day = last
    while day >= first:
        if days.get(day.isoformat(), 0) > 0:
            cur_end = cur_end or day
            cur_len += 1
        elif day != last:
            break
        day -= timedelta(days=1)
    cur_start = cur_end - timedelta(days=cur_len - 1) if cur_len else None
    return best, (cur_len, cur_start, cur_end)


def fmt(d):
    return d.strftime("%b %-d, %Y") if d else "—"


def monthly(days, months=12):
    buckets = OrderedDict()
    for iso in sorted(days):
        buckets[iso[:7]] = buckets.get(iso[:7], 0) + days[iso]
    return list(buckets.items())[-months:]


def render(s):
    (long_len, long_a, long_b), (cur_len, cur_a, cur_b) = streaks(s["days"])
    series = monthly(s["days"])
    labels = ", ".join(date.fromisoformat(f"{k}-01").strftime("%b") for k, _ in series)
    values = ", ".join(str(v) for _, v in series)
    ceiling = max((v for _, v in series), default=0)
    ceiling = max(10, ceiling + max(5, ceiling // 8))
    last_year = sum(v for _, v in series)

    top = sorted(s["langs"].items(), key=lambda kv: kv[1], reverse=True)[:8]
    total_share = sum(v for _, v in top) or 1
    rows = []
    for name, size in top:
        pct = 100 * size / total_share
        rows.append(f"| {name} | `{'█' * round(pct / 2.5)}` | {pct:.1f}% |")

    note = "" if s["restricted"] else (
        "\n> [!NOTE]\n"
        "> Counts reflect public activity only. Private contributions are hidden until\n"
        "> *Settings → Public profile → Include private contributions on my profile* is enabled.\n"
    )

    return f"""### Contributions

```mermaid
xychart-beta
    title "Contributions per month"
    x-axis [{labels}]
    y-axis "Contributions" 0 --> {ceiling}
    bar [{values}]
```

| | Total contributions | Current streak | Longest streak | Last 12 months |
|---|---|---|---|---|
| **Activity** | **{s['total']:,}** <br /><sub>{fmt(s['created'].date())} – present</sub> | **{cur_len}** {'day' if cur_len == 1 else 'days'} <br /><sub>{fmt(cur_a)}{' – ' + fmt(cur_b) if cur_len else ''}</sub> | **{long_len}** {'day' if long_len == 1 else 'days'} <br /><sub>{fmt(long_a)} – {fmt(long_b)}</sub> | **{last_year:,}** |
| **Presence** | **{s['repos']}** repositories | **{s['stars']}** stars earned | **{s['followers']}** followers | **{datetime.now(timezone.utc).year - s['created'].year}** years on GitHub |

### Most used languages

| Language | | Share |
|---|---|--:|
{chr(10).join(rows)}

<sub>Normalised per repository, so a single asset-heavy repo can't dominate. Regenerated by <a href="scripts/generate_stats.py"><code>scripts/generate_stats.py</code></a>.</sub>
{note}"""


def main():
    s = fetch()
    body = render(s)
    text = README.read_text()
    if START not in text or END not in text:
        sys.exit(f"markers {START} / {END} not found in README.md")
    text = re.sub(
        rf"{re.escape(START)}.*?{re.escape(END)}",
        f"{START}\n{body}\n{END}",
        text,
        flags=re.S,
    )
    README.write_text(text)
    (long_len, _, _), (cur_len, _, _) = streaks(s["days"])
    print(f"total={s['total']} restricted={s['restricted']} current={cur_len} "
          f"longest={long_len} repos={s['repos']} stars={s['stars']}")
    if not s["restricted"]:
        print("note: private contributions are invisible to the API — enable the profile "
              "setting to have them counted.")


if __name__ == "__main__":
    main()
