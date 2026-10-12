import dearpygui.dearpygui as dpg

from view.canvas.canva_handler import CanvaHandler


MATERIAL_COLORS = {
    "carbon_steel": (105, 119, 130),
    "aluminum": (194, 201, 204),
    "copper": (184, 91, 54),
    "brass": (190, 152, 57),
    "cast_iron": (83, 89, 92),
}


def _text_color_for_background(background):
    def luminance_component(value):
        value = value / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    luminance = sum(
        component * weight
        for component, weight in zip(
            (luminance_component(value) for value in background),
            (0.2126, 0.7152, 0.0722),
        )
    )
    white_contrast = 1.05 / (luminance + 0.05)
    black_contrast = (luminance + 0.05) / 0.05
    return (255, 255, 255) if white_contrast > black_contrast else (0, 0, 0)


class ConductionCanvas(CanvaHandler):
    def __init__(self, parent, width, height, offset_x, offset_y):
        self.name = f"conduction_canvas_{id(self)}"
        super().__init__(parent, width, height, offset_x, offset_y)

    def _initial_draw(self):
        with dpg.draw_layer(tag=f"conduction_results_{id(self)}", parent=self.name):
            pass

    def show_wall(self, data):
        self._clear_drawing()
        layers = data.get("layers", [])
        if not layers:
            return

        left = 30
        width = max(1, self.width - 60)
        top = 30
        height = max(1, self.height - 60)
        is_parallel = data.get("configuration") == "parallel"

        for index, layer in enumerate(layers):
            if is_parallel:
                x0, x1 = left, left + width
                y0 = top + height * index / len(layers)
                y1 = top + height * (index + 1) / len(layers)
            else:
                x0 = left + width * index / len(layers)
                x1 = left + width * (index + 1) / len(layers)
                y0, y1 = top + height * 0.25, top + height * 0.75

            material = layer["material"]
            fill = MATERIAL_COLORS.get(material, (118, 126, 132))
            self.graphic_handler.draw_rectangle(
                [x0, y0],
                [x1, y1],
                fill=fill,
                color=(35, 39, 42),
                parent=f"conduction_results_{id(self)}",
                tag=f"conduction_layer_{index}_{id(self)}",
                current_only=True,
            )
            self.graphic_handler.draw_text(
                [x0 + 8, (y0 + y1) / 2 - 10],
                f"Layer {index + 1}: {material.replace('_', ' ').title()}",
                color=_text_color_for_background(fill),
                parent=f"conduction_results_{id(self)}",
                size=17,
                tag=f"conduction_label_{index}_{id(self)}",
                current_only=True,
            )

    def show_results(self, results):
        self.show_wall(results)
        group = f"conduction_results_{id(self)}"
        self.graphic_handler.draw_text(
            [30, 8],
            f"R total = {results['total_resistance']:.6g} K/W   |   q = {results['heat_flux']:.6g} W/m² | Q = {results['heat_exchanged']:.6g} J",
            color=(255, 255, 255),
            parent=group,
            size=17,
            tag=f"conduction_summary_{id(self)}",
            current_only=True,
        )

    def clear_results(self):
        self._clear_drawing()

    def _clear_drawing(self):
        dpg.delete_item(f"conduction_results_{id(self)}", children_only=True)
        self.graphic_handler.command_set.clear()