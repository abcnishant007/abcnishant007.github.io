#!/usr/bin/env python3

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen


USERNAME = "abcnishant007"
SOURCE_URL = f"https://github-contributions.vercel.app/api/v1/{USERNAME}"
OUTPUT_PATH = Path("assets/data/github-contributions.json")
WEEKS_TO_KEEP = 54


def fetch_payload():
    request = Request(
        SOURCE_URL,
        headers={
            "User-Agent": "abcnishant007.github.io contribution updater",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def trim_contributions(contributions):
    today = date.today()
    cutoff = today - timedelta(days=(WEEKS_TO_KEEP * 7))
    trimmed = []
    for item in contributions:
        item_date = date.fromisoformat(item["date"])
        if item_date >= cutoff:
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

    year_summary = None
    for item in payload.get("years", []):
        if item.get("year") == current_year:
            year_summary = item
            break

    total = year_summary.get("total") if year_summary else current_year_total(trimmed)

    return {
        "username": USERNAME,
        "source": SOURCE_URL,
        "generated_at": generated_at,
        "summary": {
            "year": current_year,
            "total": total,
        },
        "contributions": trimmed,
    }


def main():
    payload = fetch_payload()
    output = build_output(payload)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
