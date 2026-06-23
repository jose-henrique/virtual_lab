import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.utils.font_manager import FontManager

class SuccessModal:
    def __init__(self):
        self.window_name = "sucess_modal_teste"
        self.width_window = 250
        self.height_window = 100
        self.pos_x = 0
        self.pos_y = 0
        self.text_font = FontManager().get("text_roboto_large")
        self.__base_window()
        
    
    def show_message(self, message):
        self.__calculate_center_position()
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True, pos=[self.pos_x, self.pos_y])
            self.__render_message(message)
    
    def __base_window(self):
        if not dpg.does_item_exist(self.window_name):
            with dpg.window(label=_("SUCCESS"), 
                tag=self.window_name,
                width=self.width_window,
                height=self.height_window,
                show=False,
                no_resize=True,
                no_collapse=True,
                pos=[self.pos_x,self.pos_y]) as window:
                    pass
    
    
    def __render_message(self, message):
        self.__clean_modal()
        dpg.add_text(message, wrap=self.width_window - 40, parent=self.window_name, tag="message")
        dpg.bind_item_font("message", self.text_font)
        
        with dpg.group(parent=self.window_name):
            dpg.add_separator()
            dpg.add_spacer(height=10)
            dpg.add_button(label="OK", width=75, callback=self.__close_window, indent=self.width_window - 120)
            
            
                    
    
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