"""Venue scheduling helpers for Rowan Gate event logistics."""

from datetime import datetime, timedelta


def parse_session_window(raw_window):
    """Parse a session window string into start and end datetimes."""
    start_raw, end_raw = raw_window.split("|")
    start = datetime.strptime(start_raw.strip(), "%Y-%m-%d %H:%M")
    end = datetime.strptime(end_raw.strip(), "%Y-%m-%d %H:%M")
    return start, end


def overlaps(existing_start, existing_end, new_start, new_end):
    """Return True when two venue bookings overlap."""
    return new_start < existing_end and existing_start < new_end


class VenueScheduler:
    """Tracks room bookings for the Rowan Gate venue."""

    def __init__(self, rooms):
        self.rooms = rooms
        self.bookings = {}

    def book(self, room_name, start, end):
        if room_name not in self.rooms:
            raise KeyError(f"Unknown room: {room_name}")
        for existing_start, existing_end in self.bookings.get(room_name, []):
            if overlaps(existing_start, existing_end, start, end):
                raise ValueError("Booking overlaps an existing reservation")
        self.bookings.setdefault(room_name, []).append((start, end))
        return True

    def turnover_gap_ok(self, room_name, start, min_gap_minutes=30):
        previous = self.bookings.get(room_name, [])
        for _, existing_end in previous:
            gap = start - existing_end
            if timedelta(0) <= gap < timedelta(minutes=min_gap_minutes):
                return False
        return True
