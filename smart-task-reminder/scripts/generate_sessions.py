"""Generate mock focused work session data for Smart Task Reminder."""
from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT_FILE = DATA_DIR / "Sessions.csv"
RNG = random.Random(42)

START_DATE = date(2024, 9, 2)  # Monday anchor for consistent 4-week window
DAYS = 28
USER_ID = "learner-001"
TASK_TYPES = ["Study", "Coding", "Writing", "Reading", "Admin"]


@dataclass
class Session:
    session_id: str
    user_id: str
    date_str: str
    start_time: str
    end_time: str
    duration_min: int
    completed: int
    abandoned: int
    tab_switches: int
    task_type: str


def _random_session_times(day_start: datetime) -> tuple[datetime, datetime, int]:
    """Generate realistic start/end times anchored to the supplied day."""
    start_offset = RNG.randint(7, 18) * 30  # 3.5 hour increments across the day
    start_dt = day_start + timedelta(minutes=start_offset)
    duration = RNG.randint(25, 120)
    end_dt = start_dt + timedelta(minutes=duration)
    return start_dt, end_dt, duration


def _completed_vs_abandoned() -> tuple[int, int]:
    total = RNG.randint(1, 4)
    completed = RNG.randint(0, total)
    abandoned = total - completed
    return completed, abandoned


def generate_sessions() -> List[Session]:
    sessions: List[Session] = []
    session_counter = 1

    for offset in range(DAYS):
        day = START_DATE + timedelta(days=offset)
        day_start = datetime.combine(day, time(5, 0))  # earliest prep window
        session_count = RNG.randint(1, 4)

        for _ in range(session_count):
            start_dt, end_dt, duration = _random_session_times(day_start)
            completed, abandoned = _completed_vs_abandoned()
            if completed == abandoned == 0:
                completed = 1

            session = Session(
                session_id=f"S{session_counter:03d}",
                user_id=USER_ID,
                date_str=day.isoformat(),
                start_time=start_dt.time().strftime("%H:%M"),
                end_time=end_dt.time().strftime("%H:%M"),
                duration_min=duration,
                completed=completed,
                abandoned=abandoned,
                tab_switches=RNG.randint(0, 25),
                task_type=RNG.choice(TASK_TYPES),
            )
            sessions.append(session)
            session_counter += 1

    return sessions


def write_sessions(rows: List[Session]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "SessionID",
                "UserID",
                "Date",
                "StartTime",
                "EndTime",
                "DurationMin",
                "CompletedCount",
                "AbandonedCount",
                "TabSwitchCount",
                "TaskType",
            ]
        )
        for session in rows:
            writer.writerow(
                [
                    session.session_id,
                    session.user_id,
                    session.date_str,
                    session.start_time,
                    session.end_time,
                    session.duration_min,
                    session.completed,
                    session.abandoned,
                    session.tab_switches,
                    session.task_type,
                ]
            )


def main() -> None:
    sessions = generate_sessions()
    write_sessions(sessions)
    print(f"Wrote {len(sessions)} sessions to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
