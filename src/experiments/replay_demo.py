
"""Sped-up playback demo: replays real sensor agent reports in time order.
"""

import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from src.agents.sensor_agent import run_sensor_agent
from src.config import MachineConfig

DELAY_SECONDS = 0.05

yaml_path = Path(__file__).parent.parent / "configs" / "t01.yaml"
with open(yaml_path) as f:
    data = yaml.safe_load(f)
config = MachineConfig(**data)

reports = run_sensor_agent(config)

failure_time = datetime(2016, 7, 18, 2, 10, tzinfo=timezone.utc)
window_start = failure_time - timedelta(days=2)
window_end = failure_time + timedelta(hours=6)

near_failure = sorted(
    (r for r in reports if window_start <= r.timestamp <= window_end),
    key=lambda r: r.timestamp,
)

print(f"replaying {len(near_failure)} points around the known failure, sped up...\n")

last_state = {}
for report in near_failure:
    key = report.internal_name
    if last_state.get(key) != report.state:
        marker = "FAILURE" if report.timestamp == failure_time else ""
        print(f"{report.timestamp}  {key:16s} -> {report.state.upper():12s} {report.reason} {marker}")
        last_state[key] = report.state
    time.sleep(DELAY_SECONDS)

print("\nreplay finished.")
