import dearpygui.dearpygui as dpg
from gettext import gettext as _
from view.simulation_window import SimulationWindow


class HomeView:
    def __init__(self):
        self.menu_bar()
        self.simulation_window = SimulationWindow()
        self.__simulation_window()
    
    def menu_bar(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label=_("File")):
                dpg.add_menu_item(label="Save")
                dpg.add_menu_item(label="Save As")
            with dpg.menu(label=_("view")):
                dpg.add_menu_item(label=_("View Simulation Window"), callback=self.__simulation_window)
                dpg.add_menu_item(label=_("View Equation Window"))
    
    def __simulation_window(self):
        self.simulation_window.base_window()


