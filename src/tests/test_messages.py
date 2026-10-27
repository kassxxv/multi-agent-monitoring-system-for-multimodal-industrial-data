from datetime import datetime

from src.messages import DeviationReport


def test_deviation_report_ok():
    report = DeviationReport(
        machine_id="T01",
        internal_name="gear_oil_temp",
        timestamp=datetime(2016, 7, 18, 2, 10),
        value=55.0,
        z_score=0.8,
        threshold=3.0,
        is_deviation=False,
        state="ok",
        reason="gear_oil_temp = 55.0°C, z-score 0.8 within threshold 3.0",
    )
    assert report.state == "ok"


def test_deviation_report_warning():
    report = DeviationReport(
        machine_id="T01",
        internal_name="gear_oil_temp",
        timestamp=datetime(2016, 7, 18, 2, 10),
        value=87.3,
        z_score=4.1,
        threshold=3.0,
        is_deviation=True,
        state="warning",
        reason="gear_oil_temp = 87.3°C, z-score 4.1 over threshold 3.0",
    )
    assert report.state == "warning"


def test_deviation_report_unavailable():
    report = DeviationReport(
        machine_id="T01",
        internal_name="gear_oil_temp",
        timestamp=datetime(2016, 7, 18, 0, 0),
        value=50.0,
        threshold=3.0,
        is_deviation=False,
        state="unavailable",
        reason="gear_oil_temp: insufficient history (need 36 points)",
    )
    assert report.z_score is None
