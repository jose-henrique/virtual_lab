import dearpygui.dearpygui as dpg
import matplotlib
import matplotlib.colors as colors

from view.canvas.canva_handler import CanvaHandler


MATERIAL_COLORS = {
    "carbon_steel": (105, 119, 130),
    "aluminum": (194, 201, 204),
    "copper": (184, 91, 54),
    "brass": (190, 152, 57),
    "cast_iron": (83, 89, 92),
    "common_brick": (156, 74, 52),
    "concrete": (150, 150, 145),
    "wood_pine": (196, 156, 102),
    "glass_wool": (232, 205, 92),
    "eps": (236, 236, 230),
}

# Minimum share of the drawing given to a layer, so very thin layers stay visible.
MIN_LAYER_FRACTION = 0.08
TEMPERATURE_STRIPS_PER_LAYER = 16


def _layer_fractions(weights):
    """Share of the drawing for each layer, proportional to its weight with a minimum size."""
    weights = [weight if weight and weight > 0 else None for weight in weights]
    if any(weight is None for weight in weights):
        weights = [1] * len(weights)
    total = sum(weights)
    fractions = [max(weight / total, MIN_LAYER_FRACTION) for weight in weights]
    total = sum(fractions)
    return [fraction / total for fraction in fractions]


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

    def _layer_boxes(self, data):
        """Rectangle of each layer: width proportional to thickness (series) or height to area (parallel)."""
        layers = data.get("layers", [])
        left = 30
        width = max(1, self.width - 60)
        top = 40
        height = max(1, self.height - 90)
        is_parallel = data.get("configuration") == "parallel"
        key = "area" if is_parallel else "thickness"
        fractions = _layer_fractions([layer.get(key) for layer in layers])

        boxes = []
        start = 0.0
        for fraction in fractions:
            end = start + fraction
            if is_parallel:
                boxes.append((left, top + height * start, left + width, top + height * end))
            else:
                boxes.append((left + width * start, top + height * 0.25, left + width * end, top + height * 0.75))
            start = end
        return boxes

    def show_wall(self, data, layer_fills=None):
        self._clear_drawing()
        layers = data.get("layers", [])
        if not layers:
            return

        group = f"conduction_results_{id(self)}"
        boxes = self._layer_boxes(data)
        for index, (layer, (x0, y0, x1, y1)) in enumerate(zip(layers, boxes)):
            material = layer["material"]
            fill = MATERIAL_COLORS.get(material, (118, 126, 132))
            self.graphic_handler.draw_rectangle(
                [x0, y0],
                [x1, y1],
                fill=fill,
                color=(35, 39, 42),
                parent=group,
                tag=f"conduction_layer_{index}_{id(self)}",
                current_only=True,
            )
            if layer_fills:
                layer_fills(index, layer, (x0, y0, x1, y1))
            label_background = fill if not layer_fills else (128, 128, 128)
            name = material.replace('_', ' ').title()
            label = f"Layer {index + 1}: {name}" if (x1 - x0) > 9 * (len(name) + 9) else f"{index + 1}"
            self.graphic_handler.draw_text(
                [x0 + 8, (y0 + y1) / 2 - 10],
                label,
                color=_text_color_for_background(label_background),
                parent=group,
                size=17,
                tag=f"conduction_label_{index}_{id(self)}",
                current_only=True,
            )

    def show_results(self, results):
        group = f"conduction_results_{id(self)}"
        hot = results.get("hot_temperature")
        cold = results.get("cold_temperature")
        is_parallel = results.get("configuration") == "parallel"
        profile = results.get("profile", [])
        has_temperatures = (
            hot is not None and cold is not None
            and (is_parallel or len(profile) == len(results.get("layers", [])) + 1)
        )
        normalize = colors.Normalize(vmin=cold, vmax=hot) if has_temperatures else None
        cmap = matplotlib.colormaps["coolwarm"]

        def temperature_color(temperature):
            return tuple(int(255 * c) for c in cmap(normalize(temperature))[:3])

        def fill_with_temperature(index, layer, box):
            # Linear temperature drop inside each layer (steady 1-D conduction, constant k).
            x0, y0, x1, y1 = box
            if is_parallel:
                t_start, t_end = hot, cold
            else:
                t_start, t_end = profile[index]["temperature"], profile[index + 1]["temperature"]
            strip = (x1 - x0) / TEMPERATURE_STRIPS_PER_LAYER
            for step in range(TEMPERATURE_STRIPS_PER_LAYER):
                fraction = (step + 0.5) / TEMPERATURE_STRIPS_PER_LAYER
                temperature = t_start + (t_end - t_start) * fraction
                fill = temperature_color(temperature)
                self.graphic_handler.draw_rectangle(
                    [x0 + strip * step, y0],
                    [x0 + strip * (step + 1), y1],
                    fill=fill,
                    color=fill,
                    parent=group,
                    tag=f"conduction_strip_{index}_{step}_{id(self)}",
                    current_only=True,
                )
            self.graphic_handler.draw_rectangle(
                [x0, y0], [x1, y1], color=(35, 39, 42), parent=group,
                tag=f"conduction_border_{index}_{id(self)}", current_only=True,
            )

        self.show_wall(results, layer_fills=fill_with_temperature if has_temperatures else None)

        if has_temperatures and not is_parallel:
            boxes = self._layer_boxes(results)
            edges = [boxes[0][0]] + [box[2] for box in boxes]
            bottom = boxes[0][3]
            for index, (x, point) in enumerate(zip(edges, profile)):
                self.graphic_handler.draw_text(
                    [x - 20, bottom + 8 + (18 if index % 2 else 0)],
                    f"{point['temperature']:.1f} °C",
                    color=(255, 255, 255),
                    parent=group,
                    size=15,
                    tag=f"conduction_interface_{index}_{id(self)}",
                    current_only=True,
                )

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
