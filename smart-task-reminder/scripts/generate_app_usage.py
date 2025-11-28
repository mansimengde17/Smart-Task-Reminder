"""Generate mock application usage telemetry for Smart Task Reminder."""
from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT_FILE = DATA_DIR / "AppUsage.csv"
RNG = random.Random(123)

START_DATE = date(2024, 9, 2)
DAYS = 28
APPS = [
    ("FocusWriter", "Productivity"),
    ("VS Code", "Productivity"),
    ("Notion", "Productivity"),
    ("YouTube", "Entertainment"),
    ("TikTok", "Social"),
    ("Twitter", "Social"),
    ("Slack", "Communication"),
    ("Discord", "Social"),
    ("Chrome Research", "Productivity"),
    ("Spotify", "Entertainment"),
]


def generate_app_usage() -> List[List[str | int]]:
    rows: List[List[str | int]] = []
    for offset in range(DAYS):
        day = START_DATE + timedelta(days=offset)
        # choose 5-7 random apps per day
        day_apps = RNG.sample(APPS, k=RNG.randint(5, 7))
        day_minutes = RNG.randint(360, 600)
        weights = [RNG.randint(1, 10) for _ in day_apps]
        weight_sum = sum(weights)
        cumulative = 0
        for (app_name, category), weight in zip(day_apps, weights):
            minutes = max(5, int(day_minutes * weight / weight_sum))
            cumulative += minutes
            rows.append(
                [
                    day.isoformat(),
                    app_name,
                    category,
                    minutes,
                    "Productive" if category in {"Productivity", "Communication"} else "Distracting",
                ]
            )
    return rows


def write_csv(rows: List[List[str | int]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Date", "AppName", "Category", "Minutes", "Label"])
        writer.writerows(rows)


def main() -> None:
    rows = generate_app_usage()
    write_csv(rows)
    print(f"Wrote {len(rows)} app usage rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
