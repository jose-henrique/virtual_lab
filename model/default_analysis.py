from model.analysis_registry import AnalysisRegistry
from model.analysis_spec import AnalysisSpec
from view.analysis_views.fin_simulation_view import FinSimluationView
from controller.fin_analyses_controller import FinAnalysesController
from model.data_serializers.fin_serializer import FinSerializer
from model.chart_adapters.fin_chart_adapater import FinChartAdapter
from view.analysis_views.conduction_simulation_view import ConductionSimulationView
from controller.conduction_analyses_controller import ConductionAnalysesController
from model.data_serializers.conduction_serializer import ConductionSerializer
from model.chart_adapters.conduction_chart_adapter import ConductionChartAdapter

registry = AnalysisRegistry()

registry.register(AnalysisSpec(
    analysis_id="new_fin_simulation",
    label="FIN",
    button_label="FIN ANALYZE",
    tag="fin",
    view_factory=FinSimluationView,
    controller_factory=FinAnalysesController,
    serializer_factory=FinSerializer,
    chart_adapter_factory=FinChartAdapter
    ))

registry.register(AnalysisSpec(
    analysis_id="new_conduction_simulation",
    label="CONDUCTION",
    button_label="CONDUCTION ANALYZE",
    tag="conduction",
    view_factory=ConductionSimulationView,
    controller_factory=ConductionAnalysesController,
    serializer_factory=ConductionSerializer,
    chart_adapter_factory=ConductionChartAdapter
    ))