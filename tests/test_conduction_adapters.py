from model.chart_adapters.conduction_chart_adapter import ConductionChartAdapter
from model.data_serializers.conduction_serializer import ConductionSerializer


def test_conduction_chart_adapter_uses_temperature_profile():
    data = {"results": {"profile": [
        {"position": 0.0, "temperature": 100.0},
        {"position": 0.01, "temperature": 20.0},
    ]}}

    assert ConductionChartAdapter().get_chart_data(data) == [[0.0, 0.01], [100.0, 20.0]]


def test_conduction_serializer_includes_engineering_results():
    result = {
        "configuration": "series",
        "hot_temperature": 100.0,
        "cold_temperature": 20.0,
        "time": 2.0,
        "total_resistance": 4.0,
        "heat_rate": 20.0,
        "heat_flux": 20.0,
        "heat_exchanged": 40.0,
        "layers": [],
        "profile": [],
    }

    rows = ConductionSerializer().serialize({"analyze_data": {}, "results": result})

    assert ["Heat Rate (W)", 20.0] in rows
    assert ["Heat Exchanged (J)", 40.0] in rows