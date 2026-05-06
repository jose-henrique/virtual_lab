import dearpygui.dearpygui as dpg
from gettext import gettext as _
from controller.charts_controller import ChartsController
from model.utils.font_manager import FontManager
from model.utils.location_getter import LocationGetter
from model.analyze_state_model import state_model


class ComparisonWindowView:
    def __init__(self, height, chart_view):
        self.window_name = "comparison_window"
        self.width_window = 300
        self.height_window = height
        self.icons_font = FontManager().get("icons_solid_base")
        self.text_font = FontManager().get("text_roboto_regular_base")
        self.chart_view = chart_view
        self.charts_controller = ChartsController(chart_view)
        self.state_model = state_model
        self.options_combo = {_("empty"): None}
        
        with dpg.theme() as self.button_style:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (18, 50, 55))          
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (28, 70, 75))   
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (10, 40, 45))    
                dpg.add_theme_color(dpg.mvThemeCol_Text, (78, 205, 215))          
                
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 12)           
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)                       

    def base_window(self):
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            with dpg.child_window(label=_("COMPARISON TOOL"), tag=self.window_name,
            always_use_window_padding=True,
            height=self.height_window,
            show=True):
                
                with dpg.group(horizontal=True):
                    dpg.add_text(_("\uf0ec COMPARISON TOOL"), color=(255, 209, 102), tag="header_comparison")
                    dpg.add_spacer(width=self.width_window-190)
                dpg.add_separator()
                dpg.add_spacer(height=20)

                self.__render_options()
                    
                
            dpg.bind_item_font("header_comparison", self.icons_font) 
                
    
    def __render_options(self):
        with dpg.group(tag="experiment_a"):
            dpg.add_text(_("EXPERIMENT A"))
            dpg.add_combo(items=list(self.options_combo.keys()), tag="combo_experiment_a", width=-1)
        dpg.add_spacer(height=5)
        with dpg.group(tag="experiment_b"):
            dpg.add_text(_("EXPERIMENT B"))
            dpg.add_combo(items=list(self.options_combo.keys()), tag="combo_experiment_b", width=-1)
        dpg.add_spacer(height=25)
        dpg.add_button(label=_("COMPARE"), tag="button_compare", width=-1, callback=self.__compare_experiments)
        dpg.bind_item_theme("button_compare",self.button_style)    
            
    def __compare_experiments(self):
           self.charts_controller.generate_data_chart(None, None)
    
    def __get_folder_location(self):
        location = LocationGetter().get_location()
        dpg.set_value("data_location", location)
        
        
    def __get_user_inputs(self):
        location = dpg.get_value("data_location")
        filename = dpg.get_value("data_filename")
        return {"location": location, "filename": filename}
          
    def define_analyze_options(self):
        avaiable_analysis = self.state_model.get_avaiable_analyzes()
        options = {}
        if not avaiable_analysis:
            return []
        for k, v in avaiable_analysis.items():
            if v.get("type") == "results":
                continue
            options[v.get("name")] = k

        self.options_combo = options
        
        dpg.configure_item("combo_experiment_a", items=list(options.keys()))
        dpg.configure_item("combo_experiment_b", items=list(options.keys()))
            