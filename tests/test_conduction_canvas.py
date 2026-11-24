import pytest

from view.canvas.conduction_canvas import (
    MATERIAL_COLORS,
    ConductionCanvas,
    _text_color_for_background,
)


def _capture_canvas_draw_calls(monkeypatch):
    rectangles = []
    texts = []
    monkeypatch.setattr("view.canvas.conduction_canvas.dpg.delete_item", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        "view.canvas.conduction_canvas.dpg.draw_rectangle",
        lambda *args, **kwargs: rectangles.append((args, kwargs)),
    )
    monkeypatch.setattr(
        "view.canvas.conduction_canvas.dpg.draw_text",
        lambda *args, **kwargs: texts.append((args, kwargs)),
    )
    return rectangles, texts


def test_parallel_layers_are_drawn_as_separate_branches(monkeypatch):
    rectangles, _ = _capture_canvas_draw_calls(monkeypatch)
    canvas = ConductionCanvas("parent", 500, 300, 0, 0)

    canvas.show_wall({
        "configuration": "parallel",
        "layers": [
            {"material": "copper"},
            {"material": "aluminum"},
        ],
    })

    first_start, first_end = rectangles[0][0][:2]
    second_start, second_end = rectangles[1][0][:2]
    assert first_start[0] == second_start[0]
    assert first_end[0] == second_end[0]
    assert first_start[1] != second_start[1]


def test_series_layers_are_drawn_sequentially_with_material_colors(monkeypatch):
    rectangles, texts = _capture_canvas_draw_calls(monkeypatch)
    canvas = ConductionCanvas("parent", 500, 300, 0, 0)

    canvas.show_wall({
        "configuration": "series",
        "layers": [
            {"material": "copper"},
            {"material": "aluminum"},
        ],
    })

    first_start, first_end = rectangles[0][0][:2]
    second_start, _ = rectangles[1][0][:2]
    assert first_start[0] < second_start[0]
    assert first_end[0] == second_start[0]
    assert rectangles[0][1]["fill"] == MATERIAL_COLORS["copper"]
    assert texts[0][1]["color"] == _text_color_for_background(MATERIAL_COLORS["copper"])


def test_material_text_color_uses_black_or_white_for_contrast():
    for background in MATERIAL_COLORS.values():
        text_color = _text_color_for_background(background)
        assert text_color in ((0, 0, 0), (255, 255, 255))

def test_series_layer_width_is_proportional_to_thickness(monkeypatch):
    rectangles, _ = _capture_canvas_draw_calls(monkeypatch)
    canvas = ConductionCanvas("parent", 500, 300, 0, 0)

    canvas.show_wall({
        "configuration": "series",
        "layers": [
            {"material": "common_brick", "thickness": 100.0},
            {"material": "eps", "thickness": 50.0},
        ],
    })

    first_width = rectangles[0][0][1][0] - rectangles[0][0][0][0]
    second_width = rectangles[1][0][1][0] - rectangles[1][0][0][0]
    assert first_width == pytest.approx(2 * second_width)


def test_very_thin_layer_keeps_a_minimum_visible_width(monkeypatch):
    rectangles, _ = _capture_canvas_draw_calls(monkeypatch)
    canvas = ConductionCanvas("parent", 500, 300, 0, 0)

    canvas.show_wall({
        "configuration": "series",
        "layers": [
            {"material": "concrete", "thickness": 1000.0},
            {"material": "copper", "thickness": 0.01},
        ],
    })

    total_width = 500 - 60
    thin_width = rectangles[1][0][1][0] - rectangles[1][0][0][0]
    assert thin_width >= 0.07 * total_width


def test_results_are_colored_by_temperature(monkeypatch):
    rectangles, texts = _capture_canvas_draw_calls(monkeypatch)
    canvas = ConductionCanvas("parent", 500, 300, 0, 0)

    canvas.show_results({
        "configuration": "series",
        "hot_temperature": 100.0,
        "cold_temperature": 20.0,
        "total_resistance": 1.0,
        "heat_flux": 80.0,
        "heat_exchanged": 800.0,
        "layers": [
            {"material": "concrete", "thickness": 0.1},
            {"material": "eps", "thickness": 0.05},
        ],
        "profile": [
            {"position": 0.0, "temperature": 100.0},
            {"position": 0.1, "temperature": 90.0},
            {"position": 0.15, "temperature": 20.0},
        ],
    })

    fills = [kwargs.get("fill") for _, kwargs in rectangles if kwargs.get("fill")]
    # Hot side is reddish, cold side bluish (coolwarm colormap).
    assert fills[1][0] > fills[1][2]
    assert fills[-1][2] > fills[-1][0]
    labels = [args[1] for args, _ in texts]
    assert "90.0 °C" in labels
