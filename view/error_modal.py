import dearpygui.dearpygui as dpg
from gettext import gettext as _
class ErrorModal:
    def __init__(self):
        self.window_name = "error_modal"
        self.width_window = 500
    
    def show_errors(self, errors_array):
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            with dpg.theme() as red_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (200, 50, 50, 255))  
                        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (255, 100, 100, 255))
            
            
            with dpg.window(label=_("ERROR"), 
            tag=self.window_name,
            width=self.width_window,
            height=250,
            pos=[200,20]):
                self.__render_errors(errors_array)
            dpg.bind_item_theme(self.window_name, red_theme)

    
    def __render_errors(self, errors):
        for idx, error in enumerate(errors):
            text_name = (f"text_{idx}")
            dpg.add_text(error, parent=self.window_name, tag=text_name)