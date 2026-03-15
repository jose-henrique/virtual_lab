import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.material_property_getter import PropertiesGetter
from controller.fin_analyses_controller import FinAnalysesController
from view.experiments_options_master_view import ExperimentsOptionsMasterView


class FinAccordionView(ExperimentsOptionsMasterView):
    def __init__(self, width, parent, canva):
        self.width = width
        self.parent = parent
        self.view_name = "fin_options"
        self.canva = canva
        self.__render_accordion()
        
    def process_results(self):
        super
        controller = FinAnalysesController()
        data = self.__capture_values()
        data_analyses = controller.solve_analyses(data)
        
        if data_analyses['status'] == 0:
            self.__success_callback(data_analyses)
        else:
            self.error_callback(data_analyses['errors'])
        
    def __render_accordion(self):
        with dpg.child_window(tag=self.view_name,
            width=self.width,
            autosize_y=True,
            always_use_window_padding=True,
            show=False,
            pos=[0,100],
            parent=self.parent):
                with dpg.collapsing_header(label=_("Geometry"), default_open=True):
                    dpg.add_combo([_("Circle"), _("Rectangle")], default_value=_("Select Geometry"), tag="geometry_type")
                    with dpg.group(tag="radius_group"):
                        dpg.add_text(_("Radius (mm)"))
                        dpg.add_input_float(label="", tag="radius", min_value=0,min_clamped=True, max_value=1000, step=0.5, step_fast=1, callback=self.__update_fin_radius)
                    with dpg.group(tag="length_group"):
                        dpg.add_text(_("Length (mm)"))
                        dpg.add_input_float(label= "", tag="length", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, callback=self.__update_fin_legth)
                with dpg.collapsing_header(label=_("Physical Properties"), default_open=True):
                    properties = PropertiesGetter()
                    dpg.add_combo(properties.list_materials(), default_value=_("Select Material"), tag="material")
                with dpg.collapsing_header(label=_("Enviroment"), default_open=True):
                    dpg.add_combo([_("Calculate Convection Coefficient "), _("Give Convection Coefficient ")], default_value=_("Select Method"))
                    with dpg.group(tag="convection_group"):
                        dpg.add_text("H (KW/m².K)")
                        dpg.add_input_float(label="", tag="convection_coefficient", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, width=150)
                    with dpg.group(tag="base_temp_group"):
                        dpg.add_text(_("Base Temp. (°C)"))  
                        dpg.add_input_float(label="", tag="base_temperature", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, width=150, callback=self.__update_base_temp)
                    with dpg.group(tag="env_temp_group"):
                        dpg.add_text(_("Env. Temp. (°C)"))    
                        dpg.add_input_float(label="", tag="env_temperature", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, width=150)
                with dpg.collapsing_header(label=_("Run Simulation"), default_open=True):
                    with dpg.group(tag="nodes_group"):
                        dpg.add_text(_("Nodes"))  
                        dpg.add_input_int(label="", tag="nodes", min_value=0,min_clamped=True, max_value=10000)
                    dpg.add_combo([_("Infinity Fin"), _("Adiabatic Fin"), _("Specified Temp"), _("Specified Convetion")], default_value=_("Select Method"), tag="solve_method")

    def __capture_values(self):
        data = {
                "fin_geometry": self.__convert_geometry_type(dpg.get_value("geometry_type")),
                "solver_method": self.__convert_method(dpg.get_value("solve_method")),
                "base_temperature": dpg.get_value("base_temperature"),
                "env_temperature": dpg.get_value("env_temperature"),
                "data": {    
                    "convection_coefficient": dpg.get_value("convection_coefficient"),
                    "dimensions": {"radius": dpg.get_value("radius")},
                    "fin_length": dpg.get_value("length"),
                    "node_count": dpg.get_value("nodes"),
                    "fin_material": dpg.get_value("material")
                }
            }
        return data
        
    def __success_callback(self, data):
        self.canva.color_fin(data["temperatures"], data["base_temperature"])
    
    def __convert_method(self, method):
        if method == "Infinity Fin":
            return 1
        elif method == "Adiabatic Fin":
            return 2
        elif method == "Specified Temp":
            return 3
        elif method == "Specified Convetion":
            return 4
        
    def __convert_geometry_type(self, geometry_type):
        if geometry_type == "Rectangle":
            return 1
        elif geometry_type == "Circle":
            return 2
    
    def __update_base_temp(self):
        self.canva.set_base_temp(dpg.get_value("base_temperature"))
        
    def __update_fin_legth(self):
        self.canva.set_fin_length(dpg.get_value("length"))
    
    def __update_fin_radius(self):
        self.canva.set_fin_height(dpg.get_value("radius") * 2)