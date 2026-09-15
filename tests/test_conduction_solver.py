from model.conduction_solver import ConductionSolver
from model.material_property_getter import PropertiesGetter


def test_conduction_series_calculates_resistance_flux_and_heat():
    material = PropertiesGetter().list_materials()[0]
    conductivity = PropertiesGetter().get_material(material)["thermal_conductivity"]
    data = {
        "configuration": "series",
        "hot_temperature": 100.0,
        "cold_temperature": 20.0,
        "time": 10.0,
        "layers": [
            {"material": material, "thickness": 10.0, "area": 2.0},
            {"material": material, "thickness": 20.0, "area": 2.0},
        ],
    }

    result = ConductionSolver().solve(data)
    resistance = 0.03 / (conductivity * 2.0)
    heat_rate = 80.0 / resistance

    assert result["total_resistance"] == resistance
    assert result["heat_rate"] == heat_rate
    assert result["heat_flux"] == heat_rate / 2.0
    assert result["heat_exchanged"] == heat_rate * 10.0
    assert abs(result["profile"][-1]["temperature"] - 20.0) < 1e-12


def test_conduction_parallel_adds_branch_conductances():
    material = PropertiesGetter().list_materials()[0]
    data = {
        "configuration": "parallel",
        "hot_temperature": 80.0,
        "cold_temperature": 20.0,
        "time": 1.0,
        "layers": [
            {"material": material, "thickness": 10.0, "area": 1.0},
            {"material": material, "thickness": 20.0, "area": 1.0},
        ],
    }

    result = ConductionSolver().solve_conduction(data)

    assert result["layer_heat_rates"][0] > result["layer_heat_rates"][1]
    assert result["heat_rate"] == sum(result["layer_heat_rates"])


def test_conduction_rejects_material_outside_database():
    data = {
        "configuration": "series",
        "hot_temperature": 80.0,
        "cold_temperature": 20.0,
        "time": 1.0,
        "layers": [{"material": "unknown", "thickness": 10.0, "area": 1.0}],
    }

    solver = ConductionSolver()

    assert solver.solve(data) is False
    assert "registered" in solver.errors[0]