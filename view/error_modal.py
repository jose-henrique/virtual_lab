import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.fonts_loader import FontLoader

class ErrorModal:
    def __init__(self):
        self.window_name = "error_modal"
        self.width_window = 500
        self.height_window = 250
    
    def show_errors(self, errors_array):
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            font_loader = FontLoader(font_size=24)
            loadedFont = font_loader.load_font()
            with dpg.theme() as red_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (200, 50, 50, 255))  
                        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (255, 100, 100, 255))
            
            
            with dpg.window(label=_("ERROR"), 
            tag=self.window_name,
            width=self.width_window,
            height=self.height_window,
            modal=True,
            no_resize=True,
            pos=[200,20]) as window:
                self.__render_errors(errors_array)
                dpg.add_button(label="OK", width=75, pos=[self.width_window - 80, self.height_window - 40], user_data=window, callback=self.__close_window)
            dpg.bind_item_theme(self.window_name, red_theme)
            dpg.bind_item_font(self.window_name, loadedFont)

    
    def __render_errors(self, errors):
        for idx, error in enumerate(errors):
            text_name = (f"text_{idx}")
            dpg.add_text(error, parent=self.window_name, tag=text_name)
    
    def __close_window(self, sender, app_data, user_data):
        dpg.delete_item(self.window_name)