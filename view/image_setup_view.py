import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.fonts_loader import FontLoader

class ImageSetupView():
    def __init__(self, canva):
        self.canva = canva
        self.window_name = "image_setup"
        self.width_window = 300
        self.height_window = 300
        self.pos_x = 0
        self.pos_y = 0
        
    def base_window(self):
        self.__calculate_center_position()
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            font_loader = FontLoader(font_name="awesome-regular.otf", font_size=12)
            icons_font = font_loader.load_font()
            with dpg.window(label=_("Image Setup"), 
            tag=self.window_name,
            width=self.width_window,
            height=self.height_window,
            pos=[self.pos_x,self.pos_y]):
                self.__render_options()
                dpg.bind_item_font("button_folder",icons_font)
    
    def __render_options(self):
        with dpg.group(tag="location_group"):
            dpg.add_text(_("File Location"))
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="", default_value="C:/users/jose.ribeiro/images", tag="location", readonly=True, width=200,enabled=True)
                dpg.add_button(label="\uf07b", width=75, tag="button_folder", callback=self.__get_folder_location)
            
        
        self.__bottom_window()
            

    def __bottom_window(self):
        with dpg.group(parent=self.window_name, horizontal=True):
            dpg.add_separator(parent=self.window_name)
            dpg.add_button(label=_("SAVE"), width=75, callback=self.__save_image, parent=self.window_name, indent=self.width_window - 120)
            
    def __get_folder_location(self):
        print("hello")
        dpg.add_file_dialog(
                directory_selector=True, show=True, callback=self.__callback, tag="file_dialog_id",
                cancel_callback=self.__cancel_callback, width=700 ,height=400)
        
    
    def __callback(sender, app_data):
        print('OK was clicked.')
        print("Sender: ", sender)
        print("App Data: ", app_data['file_path_name'])

    def __cancel_callback(sender, app_data):
        print('Cancel was clicked.')
        print("Sender: ", sender)
        print("App Data: ", app_data)    
            
    def __save_image(self):
        self.canva.save_image()
          
    def __calculate_center_position(self):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        self.pos_x = (viewport_width // 2) - (self.width_window // 2)
        self.pos_y = (viewport_height // 2) - (self.height_window // 2)    