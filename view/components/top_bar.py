import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.utils.font_manager import FontManager


class TopBar:
    def __init__(self, tag, analysis_controller):
        self.height = 50
        self.analysis_controller = analysis_controller
        with dpg.theme() as self.sidebar_bg_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 255))
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
        
        with dpg.theme() as self.action_buttons:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 255)) 
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (50, 50, 50, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (20, 20, 20, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 8)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255)) 
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1.0)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (100, 100, 100, 255))
        self.__render_top_bar(tag)

    def __render_top_bar(self, tag):
        loadedFont = FontManager().get("text_roboto_bold_medium")
        icons = FontManager().get("icons_solid_small")
        with dpg.child_window(width=-1, height=self.height, tag=tag):
                dpg.add_spacer(height=5)
                with dpg.group(horizontal=True):
                    dpg.add_text(_("THERMAL ANALYSIS"), color=(255, 140, 65), tag="application_title") # Section Header
                    dpg.add_spacer(width=650)
                    dpg.add_button(label=_("\uf04b RUN ANALYSE"), tag="button_run", width=120, callback=self.analysis_controller.run_analyze)
                    dpg.add_button(label=_("\uf6dd EXPORT DATA"), tag="button_data", width=120)
                    dpg.add_button(label=_("\uf03e EXPORT IMAGE"), tag="button_image", width=120)
        dpg.bind_item_font("application_title", loadedFont)
        dpg.bind_item_font("button_run", icons)
        dpg.bind_item_theme("button_run", self.action_buttons)
        dpg.bind_item_font("button_data", icons)
        dpg.bind_item_theme("button_data", self.action_buttons)
        dpg.bind_item_font("button_image", icons)
        dpg.bind_item_theme("button_image", self.action_buttons)
        dpg.bind_item_theme(tag, self.sidebar_bg_theme)