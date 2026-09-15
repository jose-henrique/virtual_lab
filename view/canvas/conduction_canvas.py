import dearpygui.dearpygui as dpg
import matplotlib.cm as cm
import matplotlib.colors as colors

from view.canvas.canva_handler import CanvaHandler


class ConductionCanvas(CanvaHandler):
    def __init__(self, parent, width, height, offset_x, offset_y):
        self.name = f"conduction_canvas_{id(self)}"
        super().__init__(parent, width, height, offset_x, offset_y)

    def _initial_draw(self):
        with dpg.draw_layer(tag=f"conduction_results_{id(self)}", parent=self.name):
            pass

    def show_results(self, results):
        group = f"conduction_results_{id(self)}"
        dpg.delete_item(group, children_only=True)
        layers = results.get("layers", [])
        if not layers:
            return
        values = [layer["thermal_conductivity"] for layer in layers]
        normalized = colors.Normalize(vmin=min(values), vmax=max(values) or 1)
        palette = cm.get_cmap("viridis")
        left = max(30, (self.width - min(self.width - 60, 700)) / 2)
        width = min(self.width - 60, 700)
        top = self.height / 2 - 45
        layer_width = width / len(layers)
        for index, layer in enumerate(layers):
            color = tuple(int(value * 255) for value in palette(normalized(layer["thermal_conductivity"]))[:3])
            x0 = left + index * layer_width
            dpg.draw_rectangle([x0, top], [x0 + layer_width, top + 90], fill=color,
                               color=(255, 255, 255), parent=group)
            dpg.draw_text([x0 + 5, top + 35], f"L{index + 1}\n{layer['material']}",
                          color=(255, 255, 255), parent=group)
        dpg.draw_text([left, top - 30],
                  f"R total = {results['total_resistance']:.6g} K/W   |   q = {results['heat_flux']:.6g} W/m²\n"
                  f"Q = {results['heat_exchanged']:.6g} J",
                      color=(255, 255, 255), parent=group)

    def clear_results(self):
        dpg.delete_item(f"conduction_results_{id(self)}", children_only=True)