import dearpygui.dearpygui as dpg
from gettext import gettext as _
from view.simulation_window import SimulationWindow
from view.components.top_bar import TopBar
from view.components.side_bar import SideBar
from view.canvas.fin_canvas import FinCanvas


class HomeView:
    def __init__(self):
        self.main_window_name = "main_layout_window"
        self.content_continer = "conntent_container"
        with dpg.window(tag=self.main_window_name, no_title_bar=True, no_move=True):
            TopBar("top_bar")
            with dpg.group(horizontal=True, horizontal_spacing=0):
                self.sidebar = SideBar(tag="side_bar", content_container=self.content_continer)
                with dpg.child_window(tag=self.content_continer, width=-1, height=-1):
                        pass
        dpg.set_primary_window("main_layout_window", True)
    
    def __simulation_window(self):
        self.simulation_window.base_window()
        #pass


