import dearpygui.dearpygui as dpg
from gettext import gettext as _

from controller.conduction_analyses_controller import ConductionAnalysesController
from model.material_property_getter import PropertiesGetter
from view.components.input_components import InputComponents


class ConductionAccordionView:
    def __init__(self, parent, canvas, analyze_id):
        self.parent = parent
        self.canvas = canvas
        self.analyze_id = analyze_id
        self.unique_id = id(self)
        self.layers = []
        self.layer_group = f"conduction_layers_{self.unique_id}"
        self.layer_scroll = f"conduction_layers_scroll_{self.unique_id}"
        self.input_components = InputComponents()
        self.tracked_fields = []

    def render(self):
        with dpg.child_window(parent=self.parent, width=-1, height=-1, show=False, tag=f"conduction_options_{self.unique_id}"):
            dpg.add_combo([_("Series"), _("Parallel")], default_value=_("Series"),
                          tag=self.__register_field("configuration"), callback=self._on_input_changed)
            self.input_components.input_float(self.__register_field("hot_temperature"), "°C", 0.5, "Hot temperature", 0, 1000, default_val=100, callback=self._on_input_changed)
            self.input_components.input_float(self.__register_field("cold_temperature"), "°C", 0.5, "Cold temperature", 0, 1000, default_val=100, callback=self._on_input_changed)
            self.input_components.input_float(self.__register_field("time"), "s", 0.5, "Time", 0.0001, 1000, default_val=10, callback=self._on_input_changed)
            dpg.add_button(label=_("Add layer"), callback=self._add_layer)
            with dpg.child_window(height=-1, tag=self.layer_scroll):
                with dpg.group(tag=self.layer_group):
                    pass
        self._add_layer()
        self._update_visualization()

    def show_options(self):
        dpg.show_item(f"conduction_options_{self.unique_id}")

    def hide_options(self):
        dpg.hide_item(f"conduction_options_{self.unique_id}")

    def process_results(self, sender=None, app_data=None, user_data=None):
        response = self._solve_current_data(save=True)
        if response["status"] == 0:
            self.canvas.show_results(response["results"])

    def _solve_current_data(self, save=False):
        data = {
            "configuration": "series" if dpg.get_value(self.__register_field("configuration")) == _("Series") else "parallel",
            "hot_temperature": dpg.get_value(self.__register_field("hot_temperature")),
            "cold_temperature": dpg.get_value(self.__register_field("cold_temperature")),
            "time": dpg.get_value(self.__register_field("time")),
            "layers": [],
        }
        for layer in self.layers:
            data["layers"].append({
                "material": dpg.get_value(layer["material"]),
                "thickness": dpg.get_value(layer["thickness"]),
                "area": dpg.get_value(layer["area"]),
            })
        if save:
            return ConductionAnalysesController().solve_analyses({"data": data}, self.analyze_id)
        return data

    def _update_visualization(self):
        self.canvas.show_wall(self._solve_current_data())

    def _on_input_changed(self, sender=None, app_data=None, user_data=None):
        self._update_visualization()

    def get_raw_values(self):
        return None

    def set_raw_values(self, data):
        return None

    def _add_layer(self, sender=None, app_data=None, user_data=None):
        index = len(self.layers) + 1
        material = self.__register_field(f"material_{index}")
        thickness = self.__register_field(f"thickness_{index}")
        area = self.__register_field(f"area_{index}")
        materials = PropertiesGetter().list_materials()
        dpg.add_spacer(height=10, parent=self.layer_group)
        with dpg.group(parent=self.layer_group):
            dpg.add_text(f"Layer {index}", color=(150, 150, 150))
            dpg.add_combo(materials, label="",
                    tag=material, default_value=materials[0], callback=self._on_input_changed)
        self.input_components.input_float(thickness, "mm", 1, _("Thickness (mm)"), 0.0001, 1000, callback=self._on_input_changed, default_val=10, parent=self.layer_group)
        self.input_components.input_float(area, "m²", 1, _("Area (m²)"), 0.0001, 1000, callback=self._on_input_changed, default_val=1, parent=self.layer_group)
        self.layers.append({"material": material, "thickness": thickness, "area": area})
        if dpg.does_item_exist(self.layer_group):
            self._update_visualization()

        if dpg.does_item_exist(self.layer_scroll):
            max_scroll = dpg.get_y_scroll_max(self.layer_scroll)
            dpg.set_y_scroll(self.layer_scroll, max_scroll)

    def __register_field(self, base_name):
            if base_name not in self.tracked_fields:
                self.tracked_fields.append(base_name)
            return f"{base_name}_{self.unique_id}"