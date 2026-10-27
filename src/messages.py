from pydantic import BaseModel

from typing import Literal
from datetime import datetime

class DeviationReport(BaseModel):
    "Detector check result for one signal at one point of time"
    machine_id: str
    internal_name: str
    timestamp: datetime
    value: float
    z_score: float | None = None
    threshold: float
    is_deviation: bool
    state: Literal["ok", "warning", "unavailable"]
    reason: str