from typing import Dict
from txp.common.reports.section import ReportSection
from txp.common.reports.mock_double_line import MockDoubleLine
from txp.common.reports.states_forecasting import StatesForecasting
from txp.common.reports.anomaly_detection import AnomalyDetectionStates


SECTIONS_REGISTRY: Dict[str, ReportSection] = {
    MockDoubleLine.__name__: MockDoubleLine,
    StatesForecasting.__name__: StatesForecasting,
    AnomalyDetectionStates.__name__: AnomalyDetectionStates
}
