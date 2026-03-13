import dearpygui.dearpygui as dpg
from gettext import gettext as _
from controller.application_controller import ApplicationController
from model.utils.font_manager import FontManager

dpg.create_context()

fm = FontManager()
fm.load_all_fonts()

dpg.create_viewport(title="Virtual Lab")
dpg.setup_dearpygui()

ApplicationController()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()