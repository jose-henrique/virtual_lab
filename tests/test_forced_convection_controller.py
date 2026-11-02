from controller.forced_convection_analyses_controller import ForcedConvectionAnalysesController
from model.analyze_state_model import state_model


def test_controller_saves_successful_analysis(monkeypatch):
    analyze_id = "forced_convection_controller_test"
    monkeypatch.setitem(
        state_model.avaiable_analyzes,
        analyze_id,
        {"type": "new_forced_convection_simulation", "analyze_number": 1},
    )
    saved = {}

    def save_analyze(self, saved_id, analyze, analyze_data, results):
        saved.update({
            "analyze_id": saved_id,
            "analyze_data": analyze_data,
            "results": results,
        })

    monkeypatch.setattr(
        "controller.forced_convection_analyses_controller.AnalyzeModel.save_analyze",
        save_analyze,
    )
    response = ForcedConvectionAnalysesController().solve_analyses({
        "data": {
            "velocity": 0.5,
            "diameter": 0.02,
            "length": 1.0,
            "inlet_temperature": 20.0,
            "wall_temperature": 80.0,
            "density": 997.0,
            "viscosity": 0.00089,
            "thermal_conductivity": 0.6,
            "specific_heat": 4182.0,
        },
    }, analyze_id)

    assert response["status"] == 0
    assert saved["analyze_id"] == analyze_id
    assert saved["analyze_data"]["data"]["diameter"] == 0.02
    assert saved["results"]["heat_rate"] > 0