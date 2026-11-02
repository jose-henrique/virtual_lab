from view.analysis_views.forced_convection_accordion_view import ForcedConvectionAccordionView


def test_input_change_shows_setup_without_running_preview(monkeypatch):
    calls = []
    view = ForcedConvectionAccordionView.__new__(ForcedConvectionAccordionView)
    view.canvas = type("Canvas", (), {"show_setup": lambda self: calls.append("setup")})()

    def unexpected_preview(self, data):
        raise AssertionError("Input changes must not calculate preview results")

    monkeypatch.setattr(
        "view.analysis_views.forced_convection_accordion_view.ForcedConvectionAnalysesController.solve_preview",
        unexpected_preview,
    )

    view._on_input_changed()

    assert calls == ["setup"]