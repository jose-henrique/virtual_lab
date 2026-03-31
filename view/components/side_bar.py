import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.utils.font_manager import FontManager




class SideBar:
    def __init__(self, tag, content_container, analysis_controller):
        self.width = 225
        self.content_container = content_container
        self.tag = tag
        self.tabs_group = "tabs_group"
        self.icons = FontManager().get("icons_solid_base")
        self.analysis_controller = analysis_controller
        
        with dpg.theme() as self.button_new_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 140, 65, 255))        # Orange
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 160, 100, 255)) # Lighter Orange
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 100, 40, 255))   # Darker Orange
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 8)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255)) 

        with dpg.theme() as self.button_options:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (25, 25, 26, 255))        
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 160, 100, 255)) 
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 100, 40, 255)) 
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 8)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (100, 100, 100, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (255, 140, 65, 255))

        with dpg.theme() as self.tab_active:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 100, 40, 255))        
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200, 100, 40, 255)) 
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 100, 40, 255)) 
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 8)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (255, 140, 65, 255))

    def render_sidebar(self):
        loadedFont = FontManager().get("text_roboto_regular_base")
        with dpg.child_window(width=self.width, height=-1, tag=self.tag):
                dpg.add_button(label=_("+ NEW ANALYSE"), tag="button_new_analysis", width=-1, callback=self.analysis_controller.open_new_analysis_modal, user_data=self)
                with dpg.group(tag=self.tabs_group):
                    self.add_analyze(_("\uf1fe RESULTS"), "results_button","results", 30)

                
        dpg.bind_item_font("button_new_analysis", loadedFont)
        dpg.bind_item_theme("button_new_analysis",self.button_new_theme)
        

    
    def add_analyze(self, label, tag, analysis_type, space=10):
        dpg.add_spacer(height=space, parent=self.tabs_group)
        button = dpg.add_button(label=label, tag=tag, width=-1, parent=self.tabs_group, callback=self.__select_tab, user_data=analysis_type)
        dpg.bind_item_font(button, self.icons)

    def __select_tab(self, sender, app_data, user_data):
        children = dpg.get_item_children(self.tabs_group, slot=1)
        self.analysis_controller.change_active_analyze(sender,user_data, dpg.get_item_rect_size(self.content_container), self.content_container)
        for child_tag in children:
            if dpg.get_item_alias(child_tag) == sender:
                dpg.bind_item_theme(child_tag, self.tab_active)
            else:
                dpg.bind_item_theme(child_tag, self.button_options)
        
    