import dearpygui.dearpygui as dpg
from gettext import gettext as _
    
class HomeView:
    def __init__(self):
        self.menu_bar()
    
    def menu_bar(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label=_("File")):
                dpg.add_menu_item(label="Save")
                dpg.add_menu_item(label="Save As")
            with dpg.menu(label=_("view")):
                dpg.add_menu_item(label=_("View Simulation Window"), callback=self.simulation_window)
                dpg.add_menu_item(label=_("View Equation Window"))

    def simulation_window(self):
        with dpg.window(label=_("Simulation Window"), tag="simulation_window"):
            dpg.add_text("Simulation Content Here")
        dpg.set_item_width("simulation_window", 800)
        dpg.set_item_height("simulation_window", 400)
        dpg.set_item_pos("simulation_window", [200, 201])