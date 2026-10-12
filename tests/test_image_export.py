from pathlib import Path

from model.utils.image_handler import ImageHandler
from view.canvas import conduction_canvas as conduction_module


def test_conduction_canvas_records_commands_for_image_export(monkeypatch):
    canvas = conduction_module.ConductionCanvas("parent", 800, 500, 0, 0)

    rectangles = []
    texts = []

    monkeypatch.setattr(conduction_module.dpg, "delete_item", lambda *args, **kwargs: None)
    monkeypatch.setattr(conduction_module.dpg, "draw_rectangle", lambda *args, **kwargs: rectangles.append((args, kwargs)))
    monkeypatch.setattr(conduction_module.dpg, "draw_text", lambda *args, **kwargs: texts.append((args, kwargs)))

    results = {
        "total_resistance": 0.5,
        "heat_flux": 12.3,
        "heat_exchanged": 99.9,
        "layers": [
            {"material": "Concrete", "thermal_conductivity": 0.8},
            {"material": "Steel", "thermal_conductivity": 1.6},
        ],
    }

    canvas.show_results(results)

    assert canvas.graphic_handler.command_set
    assert any(command["object_type"] == "rectangle" for command in canvas.graphic_handler.command_set.values())
    assert any(command["object_type"] == "text" for command in canvas.graphic_handler.command_set.values())


def test_image_handler_saves_png_to_selected_folder(tmp_path):
    command_set = {
        "title": {
            "object_type": "text",
            "content": "Heat flow",
            "pos": (10, 20),
            "color": (255, 255, 255),
            "tag": "title",
            "current_only": False,
        }
    }

    handler = ImageHandler(
        command_set=command_set,
        original_width=200,
        original_height=100,
        offset_x=0,
        width=400,
        height=200,
        location=str(tmp_path),
        filename="exported_image",
        background_color=(0, 0, 0),
    )

    result = handler.generate_and_save()
    file_path = Path(tmp_path) / "exported_image.png"

    assert result["status"] == 0
    assert file_path.exists()
