from model.data_serializers.fin_serializer import FinSerializer

def test_fin_serializer_generates_rows():
    payload = {
        "analyze_number": 1, 
        "analyze_id": "new_fin_simulation_493dc5b3-e851-46bc-a2cb-bd5bd0785856", 
        "type": "new_fin_simulation", 
        "analyze_data": {
            "data": {
                "base_temperature": 80.0,
                "env_temperature": 25.0, 
                "temp_end_fin": 0.0, 
                "convection_coefficient": 36.0, 
                "dimensions": {"radius": 0.005, "a": 0.0, "b": 0.0}, 
                "fin_length": 0.022, "node_count": 50, 
                "fin_material": "copper"}, 
            "heat_transfer": 10.38, 
            "area": 7.85, 
            "perimeter": 0.031, 
            "fin_efficience": 66.75, 
            "fin_geometry": 2, "solver_method": 1}, 
        "results": {
            "temperatures": [
                {"point": 0.00044, "temp_distribuition": 0.98, "relative_length": 0.02, "local_temp": 79.14}, 
                {"point": 0.00088, "temp_distribuition": 0.97, "relative_length": 0.04, "local_temp": 78.29}, 
                {"point": 0.00132, "temp_distribuition": 0.95, "relative_length": 0.06, "local_temp": 77.45},
                ]
            }
        }
    
    rows = FinSerializer().serialize(payload)
    
    assert isinstance(rows, list)
    print(rows)
    assert rows[1][1] == "Fin Analysis"