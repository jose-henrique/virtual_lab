import dearpygui.dearpygui as dpg
from gettext import gettext as _
from controller.charts_controller import ChartsController
from view.canva_handler import CanvaHandler
from view.image_setup_view import ImageSetupView
from view.fin_accordion_view import FinAccordionView
from model.utils.font_manager import FontManager

class SimulationWindow:
    def __init__(self):
        self.window_name = "simulation_window"
        self.width_window = 1000
        self.canva = CanvaHandler(self.window_name,900,400,300, 0)
        self.options_width = 235
        self.active_analyse = None
        self.available_analysis = []
    
    def base_window(self):
        
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            icons_font = FontManager().get("icons_solid_small")
            with dpg.window(label=_("Analyse Window"), 
            tag=self.window_name,
            width=self.width_window,
            height=680,
            pos=[200,20]):
                self.__global_actions()
                self.__accordion_options_simulation()
                self.canva.initial_draw()
                dpg.bind_item_font("actions_group",icons_font)
            self.__context_menu()    
            
                
                
    def __show_context_menu(self):
        if dpg.is_item_focused(self.window_name):
            mouse_pos = dpg.get_drawing_mouse_pos() 
            dpg.configure_item("window_context_menu", show=True, pos=dpg.get_mouse_pos(local=False))
            
    def __global_actions(self):
        dpg.add_combo([_("Fins"), _("Forced Convection"), _("Natural Convection"), _("Conduction")], default_value=_("Select Analyse"), width=(self.options_width - 10), callback=self.__change_active_analyse)
        with dpg.group(tag="actions_group"):
            with dpg.group(horizontal=True):
                dpg.add_button(label=_("\uf04b Run Simulation"), callback=self.__process_result)
                dpg.add_button(label=_("\uf03e Save as JPG"), callback=self.__save_image)
            with dpg.group(horizontal=True):
                dpg.add_button(label=_("\uf0c5 Clone Analyse"))
                dpg.add_button(label=_("\uf201 New Chart"))    
            
    def __accordion_options_simulation(self):
        fin_options = FinAccordionView(self.options_width, self.window_name, self.canva)
        self.available_analysis.append({"name": "Fins", "instance": fin_options})    
    
    def __process_result(self):
        if self.active_analyse:
            self.active_analyse.process_results()
        
    def __change_active_analyse(self, sender, app_data):
        for analyse in self.available_analysis:
            if analyse["name"] == app_data:
                self.active_analyse = analyse["instance"]
                self.active_analyse.show_options()
            else:
                analyse["instance"].hide_options()
        
        
        
    def __new_chart(self):
        charts_handler = ChartsController()
        charts_handler.new_chart()
    
    
    def __save_image(self):
        image_setup = ImageSetupView(self.canva)
        image_setup.base_window()
    
    def __context_menu(self):
        with dpg.window(show=False, popup=True, tag="window_context_menu", no_title_bar=True):
                dpg.add_menu_item(label=_("New Chart"), callback=self.__new_chart)
                dpg.add_menu_item(label=_("Clone Window"), callback=lambda: dpg.hide_item(self.window_name))

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, callback=self.__show_context_menu)
        