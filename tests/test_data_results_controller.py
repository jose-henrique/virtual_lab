from controller.data_results_controller import DataResultsController


class _FakeStateModel:
    def get_avaiable_analyzes(self):
        return {
            "fin_1": {"name": "Fin 1", "type": "new_fin_simulation"},
            "cond_1": {"name": "Conduction 1", "type": "new_conduction_simulation"},
            "results": {"name": "Results", "type": "results"},
        }


def _controller():
    controller = DataResultsController.__new__(DataResultsController)
    controller.state_model = _FakeStateModel()
    return controller


def test_options_without_filter_list_every_analysis_except_results():
    assert _controller().define_aviable_options() == {"Fin 1": "fin_1", "Conduction 1": "cond_1"}


def test_filter_keeps_only_the_selected_analysis_type():
    assert _controller().define_aviable_options("new_fin_simulation") == {"Fin 1": "fin_1"}


def test_filter_without_matches_returns_empty_options():
    assert _controller().define_aviable_options("unknown") == {}
