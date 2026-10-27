import pytest
from pydantic import ValidationError
from src.config import SignalConfig

import yaml
from pathlib import Path
from src.config import MachineConfig
from src.core.loader import load_signals

def test_signal_config_without_reference():
    signal = SignalConfig(
        internal_name="gear_oil_temp",
        source_column="Gear_Oil_Temp_Avg",
        unit="°C",
        method="rolling_zscore",
        threshold=3.0,
        window = 36,
    )
    assert signal.reference_signal is None


def test_signal_config_with_reference():
    signal = SignalConfig(
        internal_name="gen_bear_temp",
        source_column="Gen_Bear_Temp_Avg",
        unit="°C",
        method="residual",
        threshold=3.0,
        reference_signal="grd_prod_pwr",
        window = 36,
    )
    assert signal.reference_signal == "grd_prod_pwr"

def test_signal_config_rejects_unexpected_field():
    with pytest.raises(ValidationError):
        SignalConfig(
            internal_name="gear_oil_temp",
            source_column="Gear_Oil_Temp_Avg",
            unit="°C",
            method="rolling_zscore",
            threshold=3.0,
            not_a_real_field="oops",
        )

def test_t01_yaml_loads():
    yaml_path = Path(__file__).parent.parent / "configs" / "t01.yaml"
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    config = MachineConfig(**data)
    assert config.machine_id == "T01"
    assert len(config.signals) == 2

def test_loader():
    yaml_path = Path(__file__).parent.parent / "configs" / "t01.yaml"
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    config = MachineConfig(**data)

    result = load_signals(config)

    assert result.columns.tolist() == ["Timestamp", "gear_oil_temp", "gear_bear_temp"]
    assert result["Timestamp"].is_monotonic_increasing
    assert len(result) > 2