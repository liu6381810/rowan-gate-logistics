"""Shuttle routing helpers for Rowan Gate attendee transport."""

from collections import defaultdict


class ShuttleRoute:
    """A single shuttle loop between the depot and venue stops."""

    def __init__(self, name, stops, capacity):
        self.name = name
        self.stops = stops
        self.capacity = capacity
        self.assignments = defaultdict(list)

    def assign(self, stop_name, attendee):
        if stop_name not in self.stops:
            raise KeyError(f"Stop {stop_name} is not on route {self.name}")
        self.assignments[stop_name].append(attendee)

    def over_capacity_stops(self):
        over = []
        for stop_name, riders in self.assignments.items():
            if len(riders) > self.capacity:
                over.append(stop_name)
        return over


def build_manifest(routes):
    """Build a printable pickup manifest across all routes."""
    manifest_lines = []
    for route in routes:
        manifest_lines.append(f"Route: {route.name}")
        for stop in route.stops:
            riders = route.assignments.get(stop, [])
            manifest_lines.append(f"  {stop}: {len(riders)} riders")
    return "\n".join(manifest_lines)
