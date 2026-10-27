import pandas as pd
from src.config import MachineConfig


def load_signals(config: MachineConfig) -> pd.DataFrame:
    raw = pd.read_excel(config.data_path)
    raw["Timestamp"] = pd.to_datetime(raw["Timestamp"])
    raw = raw.sort_values("Timestamp").reset_index(drop=True)

    rename_map = {signal.source_column: signal.internal_name for signal in config.signals}
    columns_to_keep = ["Timestamp"] + list(rename_map.keys())

    return raw[columns_to_keep].rename(columns=rename_map)