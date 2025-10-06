import dearpygui.dearpygui as dpg
from gettext import gettext as _
from controller.application_controller import ApplicationController

dpg.create_context()
dpg.create_viewport(title="Virtual Lab")
dpg.setup_dearpygui()

ApplicationController()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()