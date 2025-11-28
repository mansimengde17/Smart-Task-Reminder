"""Generate interruption events tied to previously generated sessions."""
from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
INPUT_FILE = DATA_DIR / "Sessions.csv"
OUTPUT_FILE = DATA_DIR / "Interruptions.csv"
RNG = random.Random(99)

CATEGORIES = ["Slack", "Email", "Call", "Meeting", "Other"]


@dataclass
class SessionWindow:
    session_id: str
    start: datetime
    end: datetime


@dataclass
class Interruption:
    interruption_id: str
    session_id: str
    category: str
    start_dt: datetime
    duration_min: int


def load_sessions() -> List[SessionWindow]:
    sessions: List[SessionWindow] = []
    with INPUT_FILE.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_dt = datetime.fromisoformat(f"{row['Date']}T{row['StartTime']}")
            end_dt = datetime.fromisoformat(f"{row['Date']}T{row['EndTime']}")
            sessions.append(
                SessionWindow(
                    session_id=row["SessionID"],
                    start=start_dt,
                    end=end_dt,
                )
            )
    return sessions


def generate_interruptions(sessions: List[SessionWindow]) -> List[Interruption]:
    interruptions: List[Interruption] = []
    counter = 1

    for session in sessions:
        event_count = RNG.randint(0, 3)
        for _ in range(event_count):
            available_minutes = int((session.end - session.start).total_seconds() // 60)
            if available_minutes <= 5:
                continue

            duration = min(RNG.randint(1, 20), available_minutes - 1)
            offset_min = RNG.randint(0, available_minutes - duration)
            start_dt = session.start + timedelta(minutes=offset_min)

            interruptions.append(
                Interruption(
                    interruption_id=f"I{counter:04d}",
                    session_id=session.session_id,
                    category=RNG.choice(CATEGORIES),
                    start_dt=start_dt,
                    duration_min=duration,
                )
            )
            counter += 1

    return interruptions


def write_interruptions(rows: List[Interruption]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["InterruptionID", "SessionID", "Category", "StartDT", "DurationMin"])
        for interruption in rows:
            writer.writerow(
                [
                    interruption.interruption_id,
                    interruption.session_id,
                    interruption.category,
                    interruption.start_dt.isoformat(),
                    interruption.duration_min,
                ]
            )


def main() -> None:
    sessions = load_sessions()
    interruptions = generate_interruptions(sessions)
    write_interruptions(interruptions)
    print(f"Wrote {len(interruptions)} interruptions to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
