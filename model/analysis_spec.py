from dataclasses import dataclass
from typing import  Callable


@dataclass
class AnalysisSpec:
    analysis_id: str
    label: str
    button_label: str
    tag: str
    view_factory: Callable
    controller_factory: Callable
    serializer_factory: Callable
    chart_adapter_factory: Callable
    active: bool = False