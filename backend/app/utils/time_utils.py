"""Time helpers for usable-layover math."""

from datetime import datetime, timedelta

# Buffer time on each end of the layover (deplane + security clearance back).
DEFAULT_BUFFER_MINUTES = 90


def usable_minutes(
    arrival: datetime,
    departure: datetime,
    buffer_minutes: int = DEFAULT_BUFFER_MINUTES,
) -> int:
    """Minutes actually usable inside a layover after buffers."""
    total = (departure - arrival).total_seconds() / 60
    return max(0, int(total - 2 * buffer_minutes))


def merge_overlaps(pairs: list[tuple[datetime, datetime]]) -> list[tuple[datetime, datetime]]:
    """Merge overlapping [start, end] windows so shared time isn't double-counted."""
    if not pairs:
        return []
    ordered = sorted(pairs)
    merged: list[list[datetime]] = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(a, b) for a, b in merged]


def overlap_minutes(
    windows: list[tuple[datetime, datetime]],
    bounds: tuple[datetime, datetime],
) -> int:
    """Sum of minutes of `windows` inside the `bounds` (after merging overlaps)."""
    lo, hi = bounds
    clipped = [
        (max(s, lo), min(e, hi)) for s, e in windows if max(s, lo) < min(e, hi)
    ]
    return sum(int((e - s).total_seconds() / 60) for s, e in merge_overlaps(clipped))


def format_countdown(minutes: int) -> str:
    """Human-friendly countdown, e.g. '1 h 25 m'."""
    h, m = divmod(max(0, minutes), 60)
    if h and m:
        return f"{h} h {m} m"
    if h:
        return f"{h} h"
    return f"{m} m"


__all__ = [
    "DEFAULT_BUFFER_MINUTES",
    "usable_minutes",
    "merge_overlaps",
    "overlap_minutes",
    "format_countdown",
    "timedelta",
    "datetime",
]
