import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.utils.font_manager import FontManager
from model.utils.location_getter import LocationGetter
from view.error_modal import ErrorModal
from view.success_modal import SuccessModal
from controller.images_controller import ImagesController


class ImageSetupView():
    def __init__(self, active_canva):
        self.window_name = "image_setup"
        self.images_controller = ImagesController(active_canva, self.window_name)
        self.width_window = 300
        self.height_window = 335
        self.icons_font = FontManager().get("icons_solid_base")
        self.text_font = FontManager().get("text_roboto_regular_base")
        self.pos_x = 0
        self.pos_y = 0
        self.resolution_mapping = {
            "SD (640x480)": (640, 480),
            "HD (1280x720)": (1280, 720),
            "FULL HD (1920x1080)": (1920, 1080),
            "QUAD HD (2560x1440)": (2560, 1440),
            "4k (3480x2160)": (3480, 2160)
        }

        self.background_color_mapping = {
            "White": (255, 255, 255),
            "Black": (0, 0, 0),
            "Transparent": (0, 0, 0, 0)
        }


    def base_window(self):
        self.__calculate_center_position()
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True, pos=[self.pos_x, self.pos_y])
        else:
            with dpg.window(label=_("EXPORT IMAGE"), modal=True, tag=self.window_name,  no_resize=True,
                        no_title_bar=True, width=self.width_window , height=self.height_window, pos=[self.pos_x, self.pos_y]):
                
                # --- CUSTOM HEADER ---
                with dpg.group(horizontal=True):
                    dpg.add_text(_("\uf03e EXPORT IMAGE"), color=(255, 140, 65), tag="header_image_setup")
                    dpg.add_spacer(width=self.width_window-190) # Push 'X' to the right
                    dpg.add_button(label="X", callback=lambda: dpg.configure_item(self.window_name, show=False), 
                                small=True)
                dpg.add_separator()
                dpg.add_spacer(height=20)

                self.__render_options()
                    
                
            dpg.bind_item_font("header_image_setup", self.icons_font)
            dpg.bind_item_font("options", self.text_font)
            dpg.bind_item_font(self.window_name,self.text_font)   
                
    
    def __render_options(self):
        with dpg.group(tag="location_group"):
            dpg.add_text(_("File Location"))
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="", default_value="", tag="location", readonly=True, width=200,enabled=True)
                dpg.add_button(label="\uf07b", width=75, tag="button_folder", callback=self.__get_folder_location)
        dpg.add_spacer(height=5)
        with dpg.group(tag="name_group"):
            dpg.add_text(_("Image Name"))
            dpg.add_input_text(label="", default_value="my_image", tag="filename", width=self.width_window-20,enabled=True)
        dpg.add_spacer(height=5)
        with dpg.group(tag="size_group", width=self.width_window-20):
            dpg.add_text(_("Image Resolution"))
            dpg.add_combo(list(self.resolution_mapping.keys()), default_value=_("Select A Resolution"), tag="image_size")
        dpg.add_spacer(height=5)
        with dpg.group(tag="background_group", width=self.width_window-20):
            dpg.add_text(_("Image Background Color"))
            dpg.add_combo(list(self.background_color_mapping.keys()), default_value=_("Select A Background"), tag="background_color")
            
        dpg.add_spacer(height=3)
        dpg.bind_item_font("button_folder",self.icons_font)    
        self.__bottom_window()
            

    def __bottom_window(self):
        with dpg.group(parent=self.window_name, horizontal=True):
            dpg.add_separator(parent=self.window_name)
            dpg.add_button(label=_("SAVE"), width=75, callback=self.__save_image, parent=self.window_name, indent=self.width_window - 100)
            
    
    def __get_folder_location(self):
        location = LocationGetter().get_location()
        dpg.set_value("location", location)
    
            
    def __save_image(self):
        user_inputs = self.__get_user_inputs()
        self.images_controller.save_image(user_inputs) 

    def __get_user_inputs(self):
        location = dpg.get_value("location")
        filename = dpg.get_value("filename")
        image_size_key = dpg.get_value("image_size")
        image_size = self.resolution_mapping.get(image_size_key, (640, 480))
        background_color = self.background_color_mapping.get(dpg.get_value("background_color"), (0, 0, 0))    
        return {"location": location, "filename": filename, "image_size": image_size, "background_color": background_color}
          
    def __calculate_center_position(self):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        self.pos_x = (viewport_width // 2) - (self.width_window // 2)
        self.pos_y = (viewport_height // 2) - (self.height_window // 2)    