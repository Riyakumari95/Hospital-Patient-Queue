
# hospital_queue.py
import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Tuple
import time

AVG_SERVICE_MIN = 10  # tweak as needed

@dataclass(order=True)
class Patient:
    priority_key: Tuple[int, float] = field(init=False, repr=False)
    severity: int           # 1 (critical) to 5 (least severe)
    name: str
    arrived_ts: float = field(default_factory=time.time)

    def __post_init__(self):
        self.priority_key = (self.severity, self.arrived_ts)

class HospitalQueue:
    def __init__(self):
        self.emergency_heap = []  # min-heap
        self.regular_q = deque()  # FIFO

    def check_in(self, name: str, severity: int):
        if severity <= 2:
            p = Patient(severity, name)
            heapq.heappush(self.emergency_heap, p)
            print(f"🚑 Emergency: {name} (severity {severity})")
        else:
            self.regular_q.append(Patient(severity, name))
            print(f"🏥 Regular: {name} (severity {severity})")

    def next_patient(self):
        if self.emergency_heap:
            p = heapq.heappop(self.emergency_heap)
            print(f"Now attending (Emergency): {p.name} (sev {p.severity})")
        elif self.regular_q:
            p = self.regular_q.popleft()
            print(f"Now attending (Regular): {p.name} (sev {p.severity})")
        else:
            print("No patients in queue.")

    def estimated_wait(self, name: str):
        for idx, p in enumerate(sorted(self.emergency_heap)):
            if p.name == name:
                mins = idx * AVG_SERVICE_MIN
                print(f"Estimated wait for {name}: ~{mins} minutes (Emergency queue position {idx}).")
                return
        pos = None
        for i, p in enumerate(self.regular_q):
            if p.name == name:
                pos = i
                break
        if pos is None:
            print("Patient not found.")
            return
        emergency_ahead = len(self.emergency_heap)
        mins = (emergency_ahead + pos) * AVG_SERVICE_MIN
        print(f"Estimated wait for {name}: ~{mins} minutes "
              f"({emergency_ahead} emergency + {pos} regular ahead).")

    def status(self):
        print(f"Emergency queue: {len(self.emergency_heap)} | Regular queue: {len(self.regular_q)}")

def main():
    h = HospitalQueue()
    while True:
        print("\n=== Hospital Queue ===")
        print("1) Check-in  2) Next patient  3) Estimate wait  4) Status  5) Exit")
        ch = input("> ").strip()
        if ch == "1":
            name = input("Name: ").strip()
            try:
                sev = int(input("Severity (1=critical .. 5=mild): ").strip())
                if not (1 <= sev <= 5): raise ValueError
                h.check_in(name, sev)
            except ValueError:
                print("❌ Enter severity 1..5")
        elif ch == "2":
            h.next_patient()
        elif ch == "3":
            h.estimated_wait(input("Patient name: ").strip())
        elif ch == "4":
            h.status()
        elif ch == "5":
            break
        else:
            print("❌ Invalid.")

if __name__ == "__main__":
    main()
