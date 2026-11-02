from model.chart_adapters.forced_convection_chart_adapter import ForcedConvectionChartAdapter
from model.data_serializers.forced_convection_serializer import ForcedConvectionSerializer


def test_chart_adapter_returns_tube_position_and_fluid_temperature():
    data = {
        "results": {
            "profile": [
                {"position": 0.0, "fluid_temperature": 20.0},
                {"position": 1.0, "fluid_temperature": 55.0},
            ],
        },
    }

    assert ForcedConvectionChartAdapter().get_chart_data(data) == [
        [0.0, 1.0],
        [20.0, 55.0],
    ]


def test_serializer_exports_inputs_results_and_profile():
    rows = ForcedConvectionSerializer().serialize({
        "results": {
            "velocity": 0.5,
            "outlet_temperature": 55.0,
            "profile": [{"position": 1.0, "fluid_temperature": 55.0, "heat_rate": 100.0}],
        },
    })

    assert ["Velocity (m/s)", 0.5] in rows
    assert ["Outlet Temperature (°C)", 55.0] in rows
    assert [1.0, 55.0, 100.0] in rows