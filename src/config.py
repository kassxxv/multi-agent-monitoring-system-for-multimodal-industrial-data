from typing import Literal

from pydantic import BaseModel

class SignalConfig(BaseModel):
    """Configuration for one monitored signal; source column, unit and detector settings."""

    model_config = {"extra": "forbid"}
    internal_name: str
    source_column: str
    unit: str
    method: Literal["rolling_zscore", "residual"]
    threshold: float
    reference_signal: str | None = None


class MachineConfig(BaseModel):
    """Configuration for one machine; data source and the signal it monitors."""

    model_config = {"extra": "forbid"}
    machine_id: str
    data_path: str
    signals: list[SignalConfig]
