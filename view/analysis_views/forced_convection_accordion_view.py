import dearpygui.dearpygui as dpg
from gettext import gettext as _

from controller.forced_convection_analyses_controller import ForcedConvectionAnalysesController
from view.components.input_components import InputComponents
from view.error_modal import ErrorModal


class ForcedConvectionAccordionView:
    def __init__(self, parent, canvas, analyze_id):
        self.parent = parent
        self.canvas = canvas
        self.analyze_id = analyze_id
        self.unique_id = id(self)
        self.view_name = f"forced_convection_options_{self.unique_id}"
        self.input_components = InputComponents()
        self.tracked_fields = []

    def render(self):
        with dpg.child_window(parent=self.parent, width=-1, height=-1, show=False, tag=self.view_name):
            with dpg.collapsing_header(label=_("Tube and Flow"), default_open=True):
                self.input_components.input_float(self._field("velocity"), "m/s", 0.1, _("Velocity"), 0.0001, 1000, default_val=0.5, callback=self._on_input_changed)
                self.input_components.input_float(self._field("diameter_mm"), "mm", 1, _("Inner Diameter"), 0.0001, 1000, default_val=20, callback=self._on_input_changed)
                self.input_components.input_float(self._field("length"), "m", 0.1, _("Tube Length"), 0.0001, 10000, default_val=1, callback=self._on_input_changed)
            with dpg.collapsing_header(label=_("Thermal Conditions"), default_open=True):
                self.input_components.input_float(self._field("inlet_temperature"), "°C", 1, _("Inlet Fluid Temperature"), -273.15, 2000, default_val=20, callback=self._on_input_changed)
                self.input_components.input_float(self._field("wall_temperature"), "°C", 1, _("Constant Wall Temperature"), -273.15, 2000, default_val=80, callback=self._on_input_changed)
            with dpg.collapsing_header(label=_("Fluid Properties"), default_open=True):
                self.input_components.input_float(self._field("density"), "kg/m³", 1, _("Density"), 0.0001, 100000, default_val=997, callback=self._on_input_changed)
                self.input_components.input_float(self._field("viscosity_mpa_s"), "mPa.s", 0.01, _("Dynamic Viscosity"), 0.0001, 100000, default_val=0.89, callback=self._on_input_changed)
                self.input_components.input_float(self._field("thermal_conductivity"), "W/m.K", 0.01, _("Thermal Conductivity"), 0.0001, 100000, default_val=0.6, callback=self._on_input_changed)
                self.input_components.input_float(self._field("specific_heat"), "J/kg.K", 1, _("Specific Heat"), 0.0001, 1000000, default_val=4182, callback=self._on_input_changed)
            dpg.add_button(label=_("Run Simulation"), callback=self.process_results)

    def show_options(self):
        dpg.show_item(self.view_name)

    def process_results(self, sender=None, app_data=None, user_data=None):
        response = self._solve_current_data(save=True)
        if response["status"] == 0:
            self.canvas.show_results(response["results"])
        else:
            ErrorModal().show_errors(response["errors"])

    def _solve_current_data(self, save=False):
        values = self.get_raw_values()
        data = {
            "velocity": values["velocity"],
            "diameter": values["diameter_mm"] / 1000,
            "length": values["length"],
            "inlet_temperature": values["inlet_temperature"],
            "wall_temperature": values["wall_temperature"],
            "density": values["density"],
            "viscosity": values["viscosity_mpa_s"] / 1000,
            "thermal_conductivity": values["thermal_conductivity"],
            "specific_heat": values["specific_heat"],
        }
        if save:
            return ForcedConvectionAnalysesController().solve_analyses({"data": data}, self.analyze_id)
        return data

    def _on_input_changed(self, sender=None, app_data=None, user_data=None):
        self.canvas.show_setup()

    def get_raw_values(self):
        return {
            field: dpg.get_value(self._field(field))
            for field in self.tracked_fields
        }

    def set_raw_values(self, data):
        if not data:
            return
        for key, value in data.items():
            tag = self._field(key)
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, value)
        self._on_input_changed()

    def _field(self, name):
        if name not in self.tracked_fields:
            self.tracked_fields.append(name)
        return f"{name}_{self.unique_id}"