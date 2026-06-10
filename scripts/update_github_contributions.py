#!/usr/bin/env python3

import json
import os
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


USERNAME = "abcnishant007"
GRAPHQL_URL = "https://api.github.com/graphql"
PUBLIC_CONTRIBUTIONS_URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_PATH = Path("assets/data/github-contributions.json")
WEEKS_TO_KEEP = 54
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            color
            contributionCount
            contributionLevel
            date
          }
        }
      }
    }
  }
}
"""
def fetch_public_contributions_html():
    today = date.today()
    cutoff = today - timedelta(days=(WEEKS_TO_KEEP * 7))
    url = f"{PUBLIC_CONTRIBUTIONS_URL}?from={cutoff.isoformat()}&to={today.isoformat()}"
    request = Request(
        url,
        headers={
            "User-Agent": "abcnishant007.github.io contribution updater",
            "Accept": "text/html",
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def fetch_graphql_payload():
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN is not set")

    payload = json.dumps(
        {
            "query": GRAPHQL_QUERY,
            "variables": {"login": USERNAME},
        }
    ).encode("utf-8")
    request = Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "User-Agent": "abcnishant007.github.io contribution updater",
            "Accept": "application/json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        result = json.load(response)

    if result.get("errors"):
        raise RuntimeError(f"GitHub GraphQL returned errors: {result['errors']}")

    return result


def normalize_graphql_payload(payload):
    user = payload.get("data", {}).get("user") or {}
    calendar = user.get("contributionsCollection", {}).get("contributionCalendar") or {}
    weeks = calendar.get("weeks") or []

    contributions = []
    for week in weeks:
        for day in week.get("contributionDays", []):
            contributions.append(
                {
                    "date": day["date"],
                    "count": int(day.get("contributionCount", 0)),
                    "color": day.get("color", "#ebedf0"),
                    "intensity": str(day.get("contributionLevel", "0")),
                }
            )

    if not contributions:
        raise RuntimeError("No contribution days returned from GitHub GraphQL")

    return {
        "source": "github_graphql",
        "contributions": contributions,
    }


def normalize_public_html(html):
    root = ET.fromstring(html)
    contributions = []
    for rect in root.iter():
        if not rect.tag.endswith("rect"):
            continue
        day = rect.attrib.get("data-date")
        count = rect.attrib.get("data-count")
        if not day or count is None:
            continue
        contributions.append(
            {
                "date": day,
                "count": int(count),
                "color": rect.attrib.get("fill", "#ebedf0"),
                "intensity": rect.attrib.get("data-level", "0"),
            }
        )

    if not contributions:
        raise RuntimeError("No contribution cells found in public GitHub HTML")

    return {
        "source": "github_public_html",
        "contributions": contributions,
    }


def trim_contributions(contributions):
    today = date.today()
    cutoff = today - timedelta(days=(WEEKS_TO_KEEP * 7))
    trimmed = []
    for item in contributions:
        item_date = date.fromisoformat(item["date"])
        if cutoff <= item_date <= today:
            trimmed.append(item)
    return sorted(trimmed, key=lambda item: item["date"])


def current_year_total(contributions):
    current_year = date.today().year
    return sum(
        item.get("count", 0)
        for item in contributions
        if date.fromisoformat(item["date"]).year == current_year
    )


def build_output(payload):
    trimmed = trim_contributions(payload.get("contributions", []))
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    current_year = str(date.today().year)

    total = current_year_total(trimmed)

    return {
        "username": USERNAME,
        "source": payload.get("source", "unknown"),
        "generated_at": generated_at,
        "summary": {
            "year": current_year,
            "total": total,
        },
        "contributions": trimmed,
    }


def main():
    try:
        payload = normalize_graphql_payload(fetch_graphql_payload())
    except (RuntimeError, URLError, TimeoutError):
        try:
            payload = normalize_public_html(fetch_public_contributions_html())
        except (RuntimeError, URLError, TimeoutError, ET.ParseError):
            raise RuntimeError("Unable to fetch GitHub contribution data from GitHub")
    output = build_output(payload)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
