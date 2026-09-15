from model.chart_adapters.fin_chart_adapater import FinChartAdapter

def test_fin_chart_adapter_builds_xy_series():
    data = {
        "results": {
            "temperatures": [
                {"point": 0.00044, "temp_distribuition": 0.98, "relative_length": 0.02, "local_temp": 79.14}, 
                {"point": 0.00088, "temp_distribuition": 0.97, "relative_length": 0.04, "local_temp": 78.29}, 
                {"point": 0.00132, "temp_distribuition": 0.95, "relative_length": 0.06, "local_temp": 77.45},
                ]
            }
    }
    
    output = FinChartAdapter().get_chart_data(data)
    print(output)
    assert len(output) == 2
    assert output[0] == [ 0.02, 0.04, 0.06 ]
    assert output[1] == [ 79.14, 78.29, 77.45 ]