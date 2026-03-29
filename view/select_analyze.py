import dearpygui.dearpygui as dpg
from gettext import gettext as _

from model.utils.font_manager import FontManager

class SelectAnalyze:
    def __init__(self, sidebar, analysis_options, controller):
        self.modal_name = "select_analyze_modal"
        self.icons = FontManager().get("icons_solid_base")
        self.loadedFont = FontManager().get("text_roboto_regular_base")
        self.width_window = 400
        self.height_window = 250
        self.pos_x = 0
        self.pos_y = 0
        self.sidebar = sidebar
        self.analzis_options = analysis_options
        self.analysis_controller = controller

        with dpg.theme() as self.button_new_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 140, 65, 255))        # Orange
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 160, 100, 255)) # Lighter Orange
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 100, 40, 255))   # Darker Orange
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 8)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))

    def render_modal(self):
        self.__calculate_center_position()
        if dpg.does_item_exist(self.modal_name):
            dpg.configure_item(self.modal_name, show=True, pos=[self.pos_x, self.pos_y])
        else:
            with dpg.window(label=_("SELECT ANALYZE"), modal=True, tag=self.modal_name, 
                        no_title_bar=True, width=self.width_window , height=self.height_window, pos=[self.pos_x, self.pos_y]):
                
                # --- CUSTOM HEADER ---
                with dpg.group(horizontal=True):
                    dpg.add_text("\uf2c9 NEW ANALYZE", color=(255, 140, 65), tag="header_title")
                    dpg.add_spacer(width=self.width_window-190) # Push 'X' to the right
                    dpg.add_button(label="X", callback=lambda: dpg.configure_item(self.modal_name, show=False), 
                                small=True)
                dpg.add_separator()
                dpg.add_spacer(height=20)

                # --- SETTINGS SECTION ---
                with dpg.group(tag="options"):
                    for analyze in self.analzis_options.keys():
                        dpg.add_button(label=self.analzis_options[analyze].get("button"), tag=analyze, width=-1, callback=self.__selected_analyze)
                    

            dpg.bind_item_font("header_title", self.icons)
            dpg.bind_item_font("options", self.loadedFont)
            dpg.bind_item_theme("options", self.button_new_theme)

    def __calculate_center_position(self):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        self.pos_x = (viewport_width // 2) - (self.width_window // 2)
        self.pos_y = (viewport_height // 2) - (self.height_window // 2)

    def __selected_analyze(self, sender, app_data, user_data):
        self.analysis_controller.add_new_analyse(self.sidebar, sender)
        dpg.configure_item(self.modal_name, show=False)