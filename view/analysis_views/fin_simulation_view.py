import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.utils.font_manager import FontManager
from view.analysis_views.fin_accordion_view import FinAccordionView
from  view.canvas.fin_canvas import FinCanvas

class FinSimluationView:

    def __init__(self, parent, width, height):
        self.parent = parent
        self.width = width
        self.height = height
        self.__render_simulation()
    

    def __render_simulation(self):
        with dpg.group(horizontal=True, width=self.width, height=self.height, parent=self.parent):
            canvas = FinCanvas("", 200, -1, 0, 0)
            canvas.setup_canvas()
            FinAccordionView(10, "", canvas).show_options()

