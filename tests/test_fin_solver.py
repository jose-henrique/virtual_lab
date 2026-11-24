import math

import pytest

from model.fin_solver import FinSolver

# Barra circular de cobre (k = 401 W/m.K), r = 2 mm, h = 20 W/m².K (Tabela 1 do TCC).
K_COPPER = 401
RADIUS = 0.002
H = 20
PERIMETER = 2 * math.pi * RADIUS
AREA = math.pi * RADIUS ** 2
M_EXPECTED = math.sqrt(H * PERIMETER / (K_COPPER * AREA))


def _data(length=0.2, h=H, temp_end_fin=None, node_count=50):
    data = {
        "base_temperature": 100.0,
        "env_temperature": 25.0,
        "convection_coefficient": h,
        "dimensions": {"radius": RADIUS, "a": 0.0, "b": 0.0},
        "fin_length": length,
        "node_count": node_count,
        "fin_material": "copper",
    }
    if temp_end_fin is not None:
        data["temp_end_fin"] = temp_end_fin
    return data


def _solve(method, **kwargs):
    result = FinSolver(2, method).solve_fin(_data(**kwargs))
    assert result is not False
    return result


def test_m_parameter_matches_reference_value():
    # m² = hP/(kA_c) -> m ≈ 7,06 1/m para os dados da Tabela 1.
    assert M_EXPECTED == pytest.approx(7.06, abs=0.01)


def test_infinite_fin_heat_rate_and_profile():
    result = _solve(1)
    theta_b = 75.0
    q_expected = math.sqrt(H * PERIMETER * K_COPPER * AREA) * theta_b

    assert result["heat_transfer"] == pytest.approx(q_expected)
    for node in result["temp_results"]:
        assert node["temp_distribuition"] == pytest.approx(math.exp(-M_EXPECTED * node["point"]))


def test_adiabatic_tip_heat_rate_uses_tanh_of_mL():
    length = 0.2
    result = _solve(2, length=length)
    q_expected = math.sqrt(H * PERIMETER * K_COPPER * AREA) * 75.0 * math.tanh(M_EXPECTED * length)

    assert result["heat_transfer"] == pytest.approx(q_expected)
    tip = result["temp_results"][-1]
    assert tip["temp_distribuition"] == pytest.approx(1 / math.cosh(M_EXPECTED * length))


@pytest.mark.parametrize("method", [1, 2, 3, 4])
def test_profile_starts_at_base_and_ends_at_tip(method):
    result = _solve(method, temp_end_fin=40.0, length=0.2)
    nodes = result["temp_results"]

    assert len(nodes) == 50
    assert nodes[0]["point"] == 0.0
    assert nodes[0]["temp_distribuition"] == pytest.approx(1.0)
    assert nodes[-1]["point"] == pytest.approx(0.2)
    assert nodes[-1]["relative_length"] == pytest.approx(1.0)


def test_specified_tip_temperature_is_reached():
    result = _solve(3, temp_end_fin=40.0, length=0.2)

    assert result["temp_results"][-1]["temp_distribuition"] == pytest.approx((40.0 - 25.0) / 75.0)


def test_long_adiabatic_fin_approaches_infinite_fin():
    infinite = _solve(1, length=2.0)
    adiabatic = _solve(2, length=2.0)

    assert adiabatic["heat_transfer"] == pytest.approx(infinite["heat_transfer"], rel=1e-5)


def test_convective_tip_matches_adiabatic_fin_with_corrected_length():
    # Çengel: ponta com convecção ≈ ponta adiabática com Lc = L + A_c/P (= L + r/2 para seção circular).
    length = 0.2
    convective = _solve(4, length=length)
    adiabatic = _solve(2, length=length + AREA / PERIMETER)

    assert convective["heat_transfer"] == pytest.approx(adiabatic["heat_transfer"], rel=1e-3)


def test_efficiency_and_effectiveness_definitions():
    length = 0.2
    result = _solve(2, length=length)
    theta_b = 75.0
    q = result["heat_transfer"]

    assert result["fin_effectiveness"] == pytest.approx(q / (H * AREA * theta_b))
    assert result["fin_efficiency"] == pytest.approx(q / (H * PERIMETER * length * theta_b))
    # Para a ponta adiabática, η = tanh(mL)/(mL).
    assert result["fin_efficiency"] == pytest.approx(math.tanh(M_EXPECTED * length) / (M_EXPECTED * length))
    assert 0 < result["fin_efficiency"] <= 1


def test_infinite_fin_has_no_efficiency():
    assert _solve(1)["fin_efficiency"] is None
