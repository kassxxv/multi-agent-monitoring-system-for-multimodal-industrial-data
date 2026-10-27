from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from src.agents.sensor_agent import run_sensor_agent
from src.config import MachineConfig

yaml_path = Path(__file__).parent.parent / "configs" / "t01.yaml"
with open(yaml_path) as f:
    data = yaml.safe_load(f)
config = MachineConfig(**data)

reports = run_sensor_agent(config)
print(f"total reports: {len(reports)}")
print("state counts:", dict(Counter(r.state for r in reports)))

failure_time = datetime(2016, 7, 18, 2, 10, tzinfo=timezone.utc)
window_start = failure_time - timedelta(days=3)
window_end = failure_time + timedelta(days=1)

near_failure = [r for r in reports if window_start <= r.timestamp <= window_end]
warnings_near_failure = [r for r in near_failure if r.state == "warning"]

print(f"\nreports in window around failure: {len(near_failure)}")
print(f"warnings in that window: {len(warnings_near_failure)}")
for r in warnings_near_failure:
    print(r.timestamp, r.internal_name, r.reason)