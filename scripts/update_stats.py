"""Generate assets/github-activity.svg from the GitHub API.

Uses only the standard library. Reads GITHUB_USERNAME and (optionally)
GITHUB_TOKEN from the environment. Without a token the contribution
breakdown shows dashes and everything else still renders.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path

USERNAME = os.getenv("GITHUB_USERNAME", "SNEHAJUYAL")
TOKEN = os.getenv("GITHUB_TOKEN")
OUTPUT = Path(os.getenv("STATS_OUTPUT", "assets/github-activity.svg"))

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      contributionCalendar { totalContributions }
    }
  }
}
"""


def request(url: str, payload: dict | None = None) -> dict | list:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_profile() -> tuple[dict, list[dict]]:
    user = request(f"https://api.github.com/users/{USERNAME}")
    repos: list[dict] = []
    page = 1
    while True:
        batch = request(
            f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner&page={page}"
        )
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    return user, [r for r in repos if not r["fork"]]


def fetch_contributions() -> dict | None:
    if not TOKEN:
        return None
    try:
        out = request(
            "https://api.github.com/graphql",
            {"query": GRAPHQL_QUERY, "variables": {"login": USERNAME}},
        )
        return out["data"]["user"]["contributionsCollection"]
    except (urllib.error.URLError, KeyError, TypeError) as exc:
        print(f"contribution query failed: {exc}", file=sys.stderr)
        return None


def fmt(value: int | None) -> str:
    return "–" if value is None else f"{value:,}"


def render(user: dict, repos: list[dict], contrib: dict | None) -> str:
    stars = sum(r["stargazers_count"] for r in repos)
    langs = Counter(r["language"] for r in repos if r["language"])
    top_langs = langs.most_common(5)
    lang_max = max((n for _, n in top_langs), default=1)

    mix = [
        ("Commits", contrib and contrib["totalCommitContributions"]),
        ("Pull requests", contrib and contrib["totalPullRequestContributions"]),
        ("Issues", contrib and contrib["totalIssueContributions"]),
        ("Code reviews", contrib and contrib["totalPullRequestReviewContributions"]),
    ]
    mix_max = max((v or 0 for _, v in mix), default=0) or 1
    total = contrib and contrib["contributionCalendar"]["totalContributions"]

    tiles = [
        ("Original repos", len(repos)),
        ("Stars earned", stars),
        ("Followers", user["followers"]),
        ("Contributions, last year", total),
    ]

    parts: list[str] = []
    for i, (label, value) in enumerate(tiles):
        x = 24 + (i % 2) * 150
        y = 56 + (i // 2) * 74
        parts.append(
            f'<text class="num" x="{x}" y="{y + 24}">{fmt(value)}</text>'
            f'<text class="muted" x="{x}" y="{y + 44}">{escape(label)}</text>'
        )

    for i, (label, value) in enumerate(mix):
        y = 66 + i * 38
        width = 0 if not value else max(4, round(190 * value / mix_max))
        parts.append(
            f'<text class="label" x="340" y="{y}">{escape(label)}</text>'
            f'<text class="label right" x="560" y="{y}">{fmt(value)}</text>'
            f'<rect class="track" x="340" y="{y + 8}" width="220" height="6" rx="3"/>'
            f'<rect class="bar" x="340" y="{y + 8}" width="{width}" height="6" rx="3"/>'
        )

    for i, (name, count) in enumerate(top_langs):
        y = 66 + i * 30
        width = max(4, round(150 * count / lang_max))
        parts.append(
            f'<text class="label" x="610" y="{y}">{escape(name)}</text>'
            f'<text class="label right" x="780" y="{y}">{count}</text>'
            f'<rect class="track" x="610" y="{y + 8}" width="170" height="5" rx="2.5"/>'
            f'<rect class="bar2" x="610" y="{y + 8}" width="{width}" height="5" rx="2.5"/>'
        )

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = "\n  ".join(parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="820" height="250" viewBox="0 0 820 250" role="img" aria-label="GitHub activity summary for {escape(USERNAME)}">
  <style>
    :root {{ --bg:#ffffff; --border:#d0d7de; --text:#1f2328; --muted:#656d76; --track:#eaeef2; --bar:#0969da; --bar2:#1a7f37; }}
    @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d1117; --border:#30363d; --text:#e6edf3; --muted:#8b949e; --track:#21262d; --bar:#58a6ff; --bar2:#3fb950; }} }}
    text {{ font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .card {{ fill:var(--bg); stroke:var(--border); }}
    .head {{ font-size:13px; font-weight:600; fill:var(--text); }}
    .num {{ font-size:26px; font-weight:600; fill:var(--text); }}
    .muted {{ font-size:11.5px; fill:var(--muted); }}
    .label {{ font-size:12.5px; fill:var(--text); }}
    .right {{ text-anchor:end; fill:var(--muted); }}
    .track {{ fill:var(--track); }}
    .bar {{ fill:var(--bar); }}
    .bar2 {{ fill:var(--bar2); }}
  </style>
  <rect class="card" x="0.5" y="0.5" width="819" height="249" rx="8"/>
  <text class="head" x="24" y="30">Overview</text>
  <text class="head" x="340" y="30">Contribution mix, last 12 months</text>
  <text class="head" x="610" y="30">Languages across original repos</text>
  {body}
  <text class="muted" x="24" y="236">Updated {stamp} · generated by scripts/update_stats.py</text>
</svg>
"""


def main() -> None:
    user, repos = fetch_profile()
    svg = render(user, repos, fetch_contributions())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
