from model.analyze_state_model import AnalyzeStateModel

def test_state_model_add_and_active():
    state = AnalyzeStateModel()
    state.add_analyze("fin_1", {"type": "new_fin_simulation", "view": object()})
    
    assert state.get_analyze("fin_1")["type"] == "new_fin_simulation"