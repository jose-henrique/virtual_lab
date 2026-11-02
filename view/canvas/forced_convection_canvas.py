import dearpygui.dearpygui as dpg

from view.canvas.canva_handler import CanvaHandler


class ForcedConvectionCanvas(CanvaHandler):
    def __init__(self, parent, width, height, offset_x, offset_y):
        self.name = f"forced_convection_canvas_{id(self)}"
        super().__init__(parent, width, height, offset_x, offset_y)

    def _initial_draw(self):
        with dpg.draw_layer(tag=f"forced_convection_results_{id(self)}", parent=self.name):
            pass

    def show_setup(self):
        self._clear_drawing()
        group = f"forced_convection_results_{id(self)}"
        left = 45
        right = max(left + 1, self.width - 45)
        center_y = self.height * 0.52
        tube_height = max(36, min(90, self.height * 0.22))
        top = center_y - tube_height / 2
        bottom = center_y + tube_height / 2

        self.graphic_handler.draw_rectangle(
            [left, top], [right, bottom], color=(195, 205, 210), fill=(195, 205, 210),
            parent=group, tag=f"forced_tube_outer_{id(self)}", current_only=True,
        )
        self.graphic_handler.draw_rectangle(
            [left + 8, top + 8], [right - 8, bottom - 8], color=(35, 44, 49), fill=(35, 44, 49),
            parent=group, tag=f"forced_tube_inner_{id(self)}", current_only=True,
        )

    def show_experiment(self, results):
        self._clear_drawing()
        group = f"forced_convection_results_{id(self)}"
        left = 45
        right = max(left + 1, self.width - 45)
        center_y = self.height * 0.52
        tube_height = max(36, min(90, self.height * 0.22))
        top = center_y - tube_height / 2
        bottom = center_y + tube_height / 2
        profile = results.get("profile", [])
        temperatures = [point["fluid_temperature"] for point in profile]
        minimum = min(temperatures, default=0)
        maximum = max(temperatures, default=1)
        span = maximum - minimum or 1

        self.graphic_handler.draw_rectangle(
            [left, top], [right, bottom], color=(195, 205, 210), fill=(195, 205, 210),
            parent=group, tag=f"forced_tube_outer_{id(self)}", current_only=True,
        )
        self.graphic_handler.draw_rectangle(
            [left + 8, top + 8], [right - 8, bottom - 8], color=(35, 44, 49), fill=(35, 44, 49),
            parent=group, tag=f"forced_tube_inner_{id(self)}", current_only=True,
        )

        for index, point in enumerate(profile):
            x = left + 10 + (right - left - 20) * point["position"] / results["length"]
            normalized = (point["fluid_temperature"] - minimum) / span
            y = bottom - 11 - normalized * (tube_height - 22)
            if index:
                previous = profile[index - 1]
                previous_x = left + 10 + (right - left - 20) * previous["position"] / results["length"]
                previous_normalized = (previous["fluid_temperature"] - minimum) / span
                previous_y = bottom - 11 - previous_normalized * (tube_height - 22)
                self.graphic_handler.draw_line(
                    [previous_x, previous_y], [x, y], color=(255, 166, 68), thickness=3,
                    parent=group, tag=f"forced_temperature_{index}_{id(self)}", current_only=True,
                )

        self.graphic_handler.draw_text(
            [left, top - 32],
            f"Tin = {results['inlet_temperature']:.2f} °C     Tout = {results['outlet_temperature']:.2f} °C",
            color=(245, 245, 245), parent=group, size=17,
            tag=f"forced_temperature_labels_{id(self)}", current_only=True,
        )
        self.graphic_handler.draw_text(
            [left, bottom + 14],
            f"Re = {results['reynolds_number']:.4g}   Nu = {results['nusselt_number']:.4g}   h = {results['heat_transfer_coefficient']:.4g} W/m².K   q = {results['heat_rate']:.4g} W",
            color=(245, 245, 245), parent=group, size=16,
            tag=f"forced_convection_summary_{id(self)}", current_only=True,
        )

    def show_results(self, results):
        self.show_experiment(results)

    def clear_results(self):
        self._clear_drawing()

    def _clear_drawing(self):
        dpg.delete_item(f"forced_convection_results_{id(self)}", children_only=True)
        self.graphic_handler.command_set.clear()