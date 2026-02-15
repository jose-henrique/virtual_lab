import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.fonts_loader import FontLoader

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
            pos=[self.pos_x,self.pos_y]) as window:
                self.__render_errors(errors_array)
                dpg.add_button(label="OK", width=75, pos=[self.width_window - 80, self.height_window - 40], user_data=window, callback=self.__close_window)
                dpg.bind_item_theme(self.window_name, red_theme)
                dpg.bind_item_font(self.window_name, loadedFont)

    
    def __render_errors(self, errors):
        self.__clean_modal()
        for idx, error in enumerate(errors):
            text_name = (f"text_{idx}")
            dpg.add_text(error, parent=self.window_name, tag=text_name, wrap= self.width_window - 25)
            dpg.split_frame()
            text_sizes = dpg.get_item_state(text_name)['rect_size']
            window_width = dpg.get_item_state(self.window_name)['rect_size'][0]
            dpg.set_item_pos(text_name,[((window_width - text_sizes[0]) /2) - 12, ((text_sizes[1] + 20) * idx) + 50])
    
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