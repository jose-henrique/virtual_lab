import dearpygui.dearpygui as dpg
from gettext import gettext as _

from controller.conduction_analyses_controller import ConductionAnalysesController
from model.material_property_getter import PropertiesGetter


class ConductionAccordionView:
    def __init__(self, parent, canvas, analyze_id):
        self.parent = parent
        self.canvas = canvas
        self.analyze_id = analyze_id
        self.unique_id = id(self)
        self.layers = []
        self.layer_group = f"conduction_layers_{self.unique_id}"

    def render(self):
        with dpg.child_window(parent=self.parent, width=300, show=False, tag=f"conduction_options_{self.unique_id}"):
            dpg.add_combo([_("Series"), _("Parallel")], default_value=_("Series"),
                          tag=self._tag("configuration"), callback=self._on_input_changed)
            dpg.add_input_float(label=_("Hot temperature (°C)"), tag=self._tag("hot_temperature"), default_value=100,
                                callback=self._on_input_changed)
            dpg.add_input_float(label=_("Cold temperature (°C)"), tag=self._tag("cold_temperature"), default_value=20,
                                callback=self._on_input_changed)
            dpg.add_input_float(label=_("Time (s)"), tag=self._tag("time"), default_value=1, min_value=0.0001,
                                callback=self._on_input_changed)
            dpg.add_button(label=_("Add layer"), callback=self._add_layer)
            with dpg.group(tag=self.layer_group):
                pass
            dpg.add_button(label=_("Run simulation"), callback=self.process_results)
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
            "configuration": "series" if dpg.get_value(self._tag("configuration")) == "Series" else "parallel",
            "hot_temperature": dpg.get_value(self._tag("hot_temperature")),
            "cold_temperature": dpg.get_value(self._tag("cold_temperature")),
            "time": dpg.get_value(self._tag("time")),
            "layers": [],
        }
        for layer in self.layers:
            data["layers"].append({
                "material": dpg.get_value(layer["material"]),
                "thickness": dpg.get_value(layer["thickness"]),
                "area": dpg.get_value(layer["area"]),
            })
        controller = ConductionAnalysesController()
        if save:
            return controller.solve_analyses({"data": data}, self.analyze_id)
        results, errors = controller.solve_preview(data)
        return {"results": results, "errors": errors, "status": 0 if results else -1}

    def _update_visualization(self):
        response = self._solve_current_data()
        if response["status"] == 0:
            self.canvas.show_results(response["results"])
        else:
            self.canvas.clear_results()

    def _on_input_changed(self, sender=None, app_data=None, user_data=None):
        self._update_visualization()

    def get_raw_values(self):
        return None

    def set_raw_values(self, data):
        return None

    def _add_layer(self, sender=None, app_data=None, user_data=None):
        index = len(self.layers) + 1
        prefix = f"conduction_layer_{self.unique_id}_{index}"
        material = f"{prefix}_material"
        thickness = f"{prefix}_thickness"
        area = f"{prefix}_area"
        materials = PropertiesGetter().list_materials()
        dpg.add_combo(materials, label=f"Layer {index} material", parent=self.layer_group,
                  tag=material, default_value=materials[0], callback=self._on_input_changed)
        dpg.add_input_float(label=_("Thickness (mm)"), default_value=10, min_value=0.0001,
                            parent=self.layer_group, tag=thickness, callback=self._on_input_changed)
        dpg.add_input_float(label=_("Area (m²)"), default_value=1, min_value=0.0001,
                            parent=self.layer_group, tag=area, callback=self._on_input_changed)
        self.layers.append({"material": material, "thickness": thickness, "area": area})
        if dpg.does_item_exist(self.layer_group):
            self._update_visualization()

    def _tag(self, name):
        return f"conduction_{name}_{self.unique_id}"