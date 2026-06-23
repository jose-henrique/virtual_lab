import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.material_property_getter import PropertiesGetter
from controller.fin_analyses_controller import FinAnalysesController
from view.analysis_views.experiments_options_master_view import ExperimentsOptionsMasterView
from model.utils.font_manager import FontManager
from view.components.input_components import InputComponents


class FinAccordionView(ExperimentsOptionsMasterView):
    def __init__(self, width, parent, canva, analyze_id):
        super().__init__()
        self.input_components = InputComponents()
        self.width = width
        self.parent = parent
        self.analyze_id = analyze_id
        self.view_name = f"fin_options_{self.unique_id}"
        self.canva = canva
        self.loadedFont = FontManager().get("text_roboto_base")
        
        self.tracked_fields = []
        
    def process_results(self):
        super
        controller = FinAnalysesController()
        data = self.__capture_values()
        data_analyses = controller.solve_analyses(data, self.analyze_id)
        
        if data_analyses['status'] == 0:
            self.__success_callback(data_analyses)
        else:
            self.error_callback(data_analyses['errors'])
            
    def __success_callback(self, data):
        self.canva.color_fin(data["temperatures"], data["base_temperature"])
        
    def render_accordion(self):
        with dpg.child_window(tag=self.view_name,
            width=self.width,
            autosize_y=False,
            always_use_window_padding=True,
            show=False,
            parent=self.parent):
                with dpg.collapsing_header(label=_("Geometry"), default_open=True):
                    dpg.add_combo([_("Circle"), _("Rectangle")], default_value=_("Select Geometry"), tag=self.__register_field("geometry_type"), callback=self.__change_geometry)
                    self.radius = self.input_components.input_float(self.__register_field("radius"), "mm", 0.5, "Radius", 0, 1000, callback=self.__update_fin_radius,show=False)
                    with dpg.group(tag=f"square_group_{self.unique_id}", show=False):
                        self.input_components.input_float(self.__register_field("a_length"), "mm", 0.5, "A Length", 0, 1000)
                        self.input_components.input_float(self.__register_field("b_length"), "mm", 0.5, "B Length", 0, 1000)
                    self.input_components.input_float(self.__register_field("length"), "mm", 0.5, _("Length"), 0, 1000, callback=self.__update_fin_length)
                with dpg.collapsing_header(label=_("Physical Properties"), default_open=True):
                    properties = PropertiesGetter()
                    dpg.add_combo(properties.list_materials(), default_value=_("Select Material"), tag=self.__register_field("material"))
                    self.input_components.input_float(self.__register_field("base_temperature"), "°C", 0.5, _("Base Temperature"), 0, 1000, callback=self.__update_base_temp)
                    self.input_components.input_float(self.__register_field("end_temp_fin"), "°C", 0.5, _("Temp at the of the fin"), 0, 1000)
                with dpg.collapsing_header(label=_("Enviroment"), default_open=True):
                    self.input_components.input_float(self.__register_field("convection_coefficient"), "KW/m².K", 0.5, _("Convection Coefficient"), 0, 1000)
                    self.input_components.input_float(self.__register_field("env_temperature"), "°C", 0.5, _("Env. Temp."), 0, 1000)
                with dpg.collapsing_header(label=_("Run Simulation"), default_open=True):
                    self.input_components.input_int(self.__register_field("nodes"), "N", 1, _("Nodes"), 0, 1000)
                    dpg.add_combo([_("Infinity Fin"), _("Adiabatic Fin"), _("Specified Temp"), _("Specified Convetion")], default_value=_("Select Method"), tag=self.__register_field("solve_method"))
        dpg.bind_item_font(self.view_name, self.loadedFont)

    def get_raw_values(self):
        
        return {field: dpg.get_value(f"{field}_{self.unique_id}") for field in self.tracked_fields}
        
    def set_raw_values(self, data):
        if not data:
            return
        
        for key, value in data.items():
            tag = f"{key}_{self.unique_id}"
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, value)
                
        self.__change_geometry(None, data.get("geometry_type"))
        self.canva.set_base_temp(data.get("base_temperature", 0))
        self.canva.set_fin_length(data.get("length", 0))
        if data.get("geometry_type") == "Circle":
            self.canva.set_fin_height(data.get("radius", 0) * 2)
        
    def __capture_values(self):
        data = {
                "fin_geometry": self.__convert_geometry_type(dpg.get_value(f"geometry_type_{self.unique_id}")),
                "solver_method": self.__convert_method(dpg.get_value(f"solve_method_{self.unique_id}")),
                "data": {    
                    "base_temperature": dpg.get_value(f"base_temperature_{self.unique_id}"),
                    "env_temperature": dpg.get_value(f"env_temperature_{self.unique_id}"),
                    "temp_end_fin": dpg.get_value(f"end_temp_fin_{self.unique_id}"),
                    "convection_coefficient": dpg.get_value(f"convection_coefficient_{self.unique_id}"),
                    "dimensions": {"radius": dpg.get_value(f"radius_{self.unique_id}"), "a": dpg.get_value(f"a_length_{self.unique_id}"),"b": dpg.get_value(f"b_length_{self.unique_id}")},
                    "fin_length": dpg.get_value(f"length_{self.unique_id}"),
                    "node_count": dpg.get_value(f"nodes_{self.unique_id}"),
                    "fin_material": dpg.get_value(f"material_{self.unique_id}")
                }
            }
        return data
        
    
    
    def __convert_method(self, method):
        if method == "Infinity Fin":
            return 1
        elif method == "Adiabatic Fin":
            return 2
        elif method == "Specified Temp":
            return 3
        elif method == "Specified Convetion":
            return 4
        
    def __change_geometry(self, sender, geometry_type):
        if geometry_type == "Rectangle":
            dpg.show_item(f"square_group_{self.unique_id}")
            dpg.hide_item(self.radius)
        elif geometry_type == "Circle":
            dpg.show_item(self.radius)
            dpg.hide_item(f"square_group_{self.unique_id}")

    def __convert_geometry_type(self, geometry_type):
        if geometry_type == "Rectangle":
            return 1
        elif geometry_type == "Circle":
            return 2
    
    def __update_base_temp(self, tag, new_value, user_data):
        self.canva.set_base_temp(new_value)
        
    def __update_fin_length(self, tag, new_value, user_data):
        self.canva.set_fin_length(new_value)
    
    def __update_fin_radius(self, tag, new_value, user_data):
        self.canva.set_fin_height(new_value * 2)
    
    def __register_field(self, base_name):
        if base_name not in self.tracked_fields:
            self.tracked_fields.append(base_name)
            
        return f"{base_name}_{self.unique_id}"