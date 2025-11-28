"""Generate an iCalendar file representing busy windows for the learner."""
from __future__ import annotations

import random
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT_FILE = DATA_DIR / "Calendar.ics"
RNG = random.Random(7)

START_DATE = date(2024, 9, 2)
DAYS = 28


class Event:
    def __init__(self, start: datetime, end: datetime, summary: str, description: str) -> None:
        self.start = start
        self.end = end
        self.summary = summary
        self.description = description

    def to_ics(self) -> str:
        start_str = self.start.strftime("%Y%m%dT%H%M%SZ")
        end_str = self.end.strftime("%Y%m%dT%H%M%SZ")
        lines = [
            "BEGIN:VEVENT",
            f"DTSTART:{start_str}",
            f"DTEND:{end_str}",
            f"SUMMARY:{self.summary}",
            f"DESCRIPTION:{self.description}",
            "END:VEVENT",
        ]
        return "\n".join(lines)


def _meeting_count(day: date) -> int:
    if day.weekday() >= 5:
        return RNG.choice([0, 0, 1])
    return RNG.randint(0, 3)


def _slot(day: date, slot_index: int) -> tuple[datetime, datetime]:
    base_hours = [9, 11, 14, 16]
    hour = base_hours[slot_index % len(base_hours)]
    start = datetime.combine(day, time(hour, RNG.choice([0, 15, 30])), tzinfo=None)
    start = start.replace(tzinfo=None)
    duration = RNG.choice([30, 45, 60, 75])
    end = start + timedelta(minutes=duration)
    return start, end


def generate_events() -> List[Event]:
    events: List[Event] = []
    for offset in range(DAYS):
        day = START_DATE + timedelta(days=offset)
        for slot in range(_meeting_count(day)):
            start, end = _slot(day, slot)
            summary = RNG.choice(
                [
                    "Standup",
                    "Advisor Sync",
                    "Team Planning",
                    "Deep Dive",
                    "Focus Block",
                ]
            )
            description = f"Auto-generated calendar block for {summary.lower()}"
            events.append(Event(start, end, summary, description))
    return events


def write_calendar(events: List[Event]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    header = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Smart Task Reminder//EN",
    ]
    body = [event.to_ics() for event in events]
    footer = ["END:VCALENDAR", ""]
    OUTPUT_FILE.write_text("\n".join(header + body + footer), encoding="utf-8")
    print(f"Wrote {len(events)} VEVENTS to {OUTPUT_FILE}")


def main() -> None:
    events = generate_events()
    write_calendar(events)


if __name__ == "__main__":
    main()
