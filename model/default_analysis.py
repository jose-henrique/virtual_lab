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
from view.analysis_views.forced_convection_simulation_view import ForcedConvectionSimulationView
from controller.forced_convection_analyses_controller import ForcedConvectionAnalysesController
from model.data_serializers.forced_convection_serializer import ForcedConvectionSerializer
from model.chart_adapters.forced_convection_chart_adapter import ForcedConvectionChartAdapter

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
    button_label="CONDUCTION",
    tag="conduction",
    view_factory=ConductionSimulationView,
    controller_factory=ConductionAnalysesController,
    serializer_factory=ConductionSerializer,
    chart_adapter_factory=ConductionChartAdapter
    ))

registry.register(AnalysisSpec(
    analysis_id="new_forced_convection_simulation",
    label="FORCED CONVECTION",
    button_label="FORCED CONVECTION",
    tag="forced_convection",
    view_factory=ForcedConvectionSimulationView,
    controller_factory=ForcedConvectionAnalysesController,
    serializer_factory=ForcedConvectionSerializer,
    chart_adapter_factory=ForcedConvectionChartAdapter
    ))