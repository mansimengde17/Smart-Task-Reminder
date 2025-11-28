"""Generate mock personal goals/progress data."""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT_FILE = DATA_DIR / "Goals.csv"

GOALS = [
    ("G001", "Finish ML coursework", 1200),
    ("G002", "Ship Smart Reminder MVP", 900),
    ("G003", "Write weekly study summary", 240),
]

START_DATE = date(2024, 9, 2)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["GoalID", "GoalName", "TargetMinutes", "ActualMinutes", "DueDate", "Status"])
        for idx, (goal_id, name, target) in enumerate(GOALS):
            actual = int(target * (0.55 + idx * 0.15))
            due_date = START_DATE + timedelta(days=21 + idx * 7)
            status = "On Track" if actual / target >= 0.7 else "At Risk"
            writer.writerow([goal_id, name, target, actual, due_date.isoformat(), status])
    print(f"Wrote {len(GOALS)} goal rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
