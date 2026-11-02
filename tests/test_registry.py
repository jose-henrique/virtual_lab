from model.default_analysis import registry

def test_fin_spec_is_registred():
    spec = registry.get("new_fin_simulation")
    assert spec is not None
    assert spec.analysis_id == "new_fin_simulation"
    assert spec.tag == "fin"
    
def test_unkown_spec_is_missing():
    spec = registry.get("unknown_analysis")
    assert spec is None

def test_forced_convection_spec_is_registered():
    spec = registry.get("new_forced_convection_simulation")
    assert spec is not None
    assert spec.tag == "forced_convection"
    assert spec.view_factory.__name__ == "ForcedConvectionSimulationView"