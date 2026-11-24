import math

from model.forced_convection_solver import ForcedConvectionSolver


def _water_data(velocity=0.5):
    return {
        "velocity": velocity,
        "diameter": 0.02,
        "length": 1.0,
        "inlet_temperature": 20.0,
        "wall_temperature": 80.0,
        "density": 997.0,
        "viscosity": 0.00089,
        "thermal_conductivity": 0.6,
        "specific_heat": 4182.0,
    }


def test_turbulent_flow_calculates_heat_transfer_and_temperature_profile():
    result = ForcedConvectionSolver().solve(_water_data())

    assert result["correlation"] == "Gnielinski"
    assert result["reynolds_number"] > 3000
    assert result["heat_transfer_coefficient"] > 0
    assert result["heat_rate"] > 0
    assert result["inlet_temperature"] == result["profile"][0]["fluid_temperature"]
    assert math.isclose(result["outlet_temperature"], result["profile"][-1]["fluid_temperature"])
    assert math.isclose(result["profile"][-1]["heat_rate"], result["heat_rate"])


def test_laminar_flow_uses_thermal_entry_correlation():
    data = _water_data(velocity=0.01)

    result = ForcedConvectionSolver().solve(data)
    re_pr = result["reynolds_number"] * result["prandtl_number"]
    graetz = (data["diameter"] / data["length"]) * re_pr
    expected = 3.66 + 0.065 * graetz / (1 + 0.04 * graetz ** (2 / 3))

    assert result["reynolds_number"] < 2300
    assert result["correlation"] == "Laminar, thermal entry (Edwards)"
    assert math.isclose(result["nusselt_number"], expected)
    assert result["nusselt_number"] > 3.66
    assert math.isclose(result["thermal_entry_length"], 0.05 * re_pr * data["diameter"])
    assert result["thermally_developing"] is True


def test_laminar_flow_in_long_tube_tends_to_fully_developed_value():
    data = _water_data(velocity=0.01)
    data["length"] = 10000.0

    result = ForcedConvectionSolver().solve(data)

    assert math.isclose(result["nusselt_number"], 3.66, rel_tol=1e-2)
    assert result["thermally_developing"] is False


def test_invalid_fluid_properties_are_rejected():
    data = _water_data()
    data["viscosity"] = 0
    solver = ForcedConvectionSolver()

    assert solver.solve(data) is False
    assert any("viscosity" in error for error in solver.errors)