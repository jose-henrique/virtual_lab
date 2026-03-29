import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.utils.font_manager import FontManager

class ErrorModal:
    def __init__(self):
        self.window_name = "error_modal"
        self.width_window = 500
        self.height_window = 250
        self.pos_x = 0
        self.pos_y = 0
    
    def show_errors(self, errors_array):
        self.__calculate_center_position()
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True, pos=[self.pos_x, self.pos_y])
            self.__render_errors(errors_array)
        else:
            loadedFont = FontManager().get("text_roboto_regular_medium")
            with dpg.theme() as orange_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (255, 145, 65, 255))  
                        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (255, 145, 65, 255))
            
            
            with dpg.window(label=_("ERROR WINDOW"), 
            tag=self.window_name,
            width=self.width_window,
            height=self.height_window,
            modal=True,
            no_resize=True,
            pos=[self.pos_x,self.pos_y]) as window:
                self.__render_errors(errors_array)
                dpg.bind_item_theme(self.window_name, orange_theme)
                dpg.bind_item_font(self.window_name, loadedFont)

    
    def __render_errors(self, errors):
        self.__clean_modal()
        for idx, error in enumerate(errors):
            with dpg.group(parent=self.window_name, horizontal=True):
                dpg.add_spacer(width=20) 
                dpg.add_text("[ERROR]: ", color=(220, 0, 0))
                dpg.add_text(error, wrap=self.width_window - 40)
        
        with dpg.group(parent=self.window_name, horizontal=True):
            dpg.add_separator(parent=self.window_name)
            dpg.add_button(label="OK", width=75, callback=self.__close_window, parent=self.window_name, indent=self.width_window - 120)
            
            
                    
    
    def __close_window(self, sender, app_data, user_data):
        dpg.configure_item(self.window_name, show=False)
        
    def __clean_modal(self):
        children = dpg.get_item_children(self.window_name, slot=1)
        for child in children:
            dpg.delete_item(child)
            
    def __calculate_center_position(self):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        self.pos_x = (viewport_width // 2) - (self.width_window // 2)
        self.pos_y = (viewport_height // 2) - (self.height_window // 2)