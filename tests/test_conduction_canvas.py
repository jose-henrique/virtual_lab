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