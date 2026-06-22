import json
import math
from datetime import datetime, timezone
from collections import defaultdict


# =========================
# TDU STREAM EVENT ENGINE
# CLEAN VERSION (NO PATCHES)
# =========================

class TDUEventStream:

    def __init__(self, persist_file=None):
        self.events = []
        self.state = defaultdict(float)
        self.persist_file = persist_file
        self.baseline_vector = None

    # =========================
    # EVENT CREATION
    # =========================
    def create_event(self, source_system, event_type, payload):

        vector = self.generate_vector_snapshot(source_system, event_type, payload)

        event = {
            "event_id": len(self.events) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_system": source_system,
            "event_type": event_type,
            "payload": payload,
            "vector": vector
        }

        self.ingest(event)
        return event

    # =========================
    # VECTOR SNAPSHOT (D1–D8 CORE)
    # =========================
    def generate_vector_snapshot(self, source_system, event_type, payload):

        text = str(payload)

        vector = {
            "d1_time_density": len(self.events) + 1,
            "d2_velocity": len(text) / 10,
            "d3_repetition": self.compute_repetition(text),
            "d4_relational": self.compute_relational_density(source_system),
            "d5_stability": self.compute_stability(source_system),
            "d6_drift": self.compute_drift(),
            "d7_complexity": len(text) / 5,
            "d8_identity": self.compute_identity_weight(source_system, payload)
        }

        return vector

    # =========================
    # INGEST PIPELINE
    # =========================
    def ingest(self, event):
        self.events.append(event)
        self.update_state(event)
        self.update_baseline()
        self.persist()

    # =========================
    # STATE RECONSTRUCTION
    # =========================
    def update_state(self, event):

        self.state["total_events"] += 1
        self.state[event["source_system"]] += 1
        self.state[f"type_{event['event_type']}"] += 1

        self.state["last_drift"] = event["vector"]["d6_drift"]

    # =========================
    # PATTERN FUNCTIONS
    # =========================
    def compute_repetition(self, text):
        return sum(1 for e in self.events if str(e["payload"]) == text)

    def compute_relational_density(self, system):
        return sum(1 for e in self.events if e["source_system"] == system)

    def compute_stability(self, system):
        vals = [
            e["vector"]["d2_velocity"]
            for e in self.events
            if e["source_system"] == system
        ]

        if len(vals) < 2:
            return 1.0

        avg = sum(vals) / len(vals)
        variance = sum((v - avg) ** 2 for v in vals) / len(vals)

        return 1 / (1 + variance)

    def compute_drift(self):
        if not self.events:
            return 0.0

        current = self.events[-1]["vector"]["d2_velocity"]
        baseline = self.baseline_vector or current

        return abs(current - baseline)

    def compute_identity_weight(self, system, payload):
        base = self.compute_relational_density(system)
        return math.log(1 + base + len(str(payload)))

    # =========================
    # BASELINE TRACKING
    # =========================
    def update_baseline(self):
        if not self.events:
            return

        self.baseline_vector = self.events[-1]["vector"]["d2_velocity"]

    # =========================
    # OUTPUT
    # =========================
    def get_state(self):
        return dict(self.state)

    def get_events(self):
        return self.events

    # =========================
    # LOCAL PERSISTENCE
    # =========================
    def persist(self):
        if not self.persist_file:
            return

        with open(self.persist_file, "w") as f:
            json.dump(self.events, f, indent=2)


# =========================
# LANDING PAD TEST RUN
# =========================
if __name__ == "__main__":

    stream = TDUEventStream(persist_file="tdu_events.json")

    stream.create_event("freelance", "task", {"task": "write proposal"})
    stream.create_event("ties", "relationship", {"person": "john_doe"})
    stream.create_event("finance", "transaction", {"amount": 250})
    stream.create_event("freelance", "task", {"task": "client followup"})

    print("\n--- STATE ---")
    print(stream.get_state())

    print("\n--- EVENTS ---")
    for e in stream.get_events():
        print(e)