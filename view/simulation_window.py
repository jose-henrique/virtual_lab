import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.material_property_getter import PropertiesGetter
from controller.fin_analyses_controller import FinAnalysesController
from controller.charts_controller import ChartsController
from view.canva_handler import CanvaHandler
from view.error_modal import ErrorModal

class SimulationWindow:
    def __init__(self):
        self.window_name = "simulation_window"
        self.width_window = 1000
        self.canva = CanvaHandler(self.window_name,900,400,300, 0)
    
    def base_window(self):
        
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            with dpg.window(label=_("Simulation Window"), 
            tag=self.window_name,
            width=self.width_window,
            height=600,
            pos=[200,20]):
                self.__accordion_options_simulation(self.window_name)
                self.canva.initial_draw()
            self.__context_menu()    
            
                
                
    def __show_context_menu(self):
        # Só mostra o menu se a janela de simulação estiver sendo focada/clicada
        if dpg.is_item_focused(self.window_name):
            # Move o menu para a posição atual do mouse
            mouse_pos = dpg.get_drawing_mouse_pos() 
            dpg.configure_item("window_context_menu", show=True, pos=dpg.get_mouse_pos(local=False))
            
    def __accordion_options_simulation(self,parent):
        with dpg.child_window(tag="accordion_simulation",
            width=300,
            autosize_y=True,
            always_use_window_padding=True,
            pos=[0,20],
            parent=parent):
                with dpg.collapsing_header(label=_("Analyse Type"), default_open=True):
                    dpg.add_combo([_("Fins"), _("Forced Convection"), _("Natural Convection"), _("Conduction")], default_value=_("Select Analyse"))
                with dpg.collapsing_header(label=_("Geometry"), default_open=True):
                    dpg.add_combo([_("Circle"), _("Rectangle")], default_value=_("Select Geometry"), tag="geometry_type")
                    dpg.add_input_float(label=_("Radius (mm)"), tag="radius", min_value=0,min_clamped=True, max_value=1000, step=0.5, step_fast=1, callback=self.__update_fin_radius)
                    dpg.add_input_float(label=_("Length (mm)"), tag="length", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, callback=self.__update_fin_legth)
                with dpg.collapsing_header(label=_("Physical Properties"), default_open=True):
                    properties = PropertiesGetter()
                    dpg.add_combo(properties.list_materials(), default_value=_("Select Material"), tag="material")
                with dpg.collapsing_header(label=_("Enviroment"), default_open=True):
                    dpg.add_combo([_("Calculate Convection Coefficient "), _("Give Convection Coefficient ")], default_value=_("Select Method"))
                    dpg.add_input_float(label="H (KW/m².K)", tag="convection_coefficient", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, width=150)
                    dpg.add_input_float(label="Base Temp. (°C)", tag="base_temperature", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, width=150, callback=self.__update_base_temp)
                    dpg.add_input_float(label="Env. Temp. (°C)", tag="env_temperature", min_value=0,min_clamped=True, max_value=10000, step=1, step_fast=10, width=150)
                with dpg.collapsing_header(label=_("Run Simulation"), default_open=True):
                    dpg.add_input_int(label="Nodes", tag="nodes", min_value=0,min_clamped=True, max_value=10000)
                    dpg.add_combo([_("Infinity Fin"), _("Adiabatic Fin"), _("Specified Temp"), _("Specified Convetion")], default_value=_("Select Method"), tag="solve_method")
                    dpg.add_button(label=_("Run Simulation"), callback=self.__capture_values)
    
    def __new_chart(self):
        charts_handler = ChartsController()
        charts_handler.new_chart()
    
    def __capture_values(self):
        controller = FinAnalysesController()
        data_analyses = controller.solve_analyses(
            {
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
        )
        
        if data_analyses['status'] == 0:
            self.__success_callback(data_analyses)
        else:
            self.__error_callback(data_analyses['errors'])
        
    def __success_callback(self, data):
        self.canva.color_fin(data["temperatures"], data["base_temperature"])
    
    def __error_callback(self, errors):
        error_modal = ErrorModal()
        error_modal.show_errors(errors)
    
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
        
    def __context_menu(self):
        with dpg.window(show=False, popup=True, tag="window_context_menu", no_title_bar=True):
                dpg.add_menu_item(label=_("New Chart"), callback=self.__new_chart)
                dpg.add_menu_item(label=_("Clone Window"), callback=lambda: dpg.hide_item(self.window_name))

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, callback=self.__show_context_menu)
        