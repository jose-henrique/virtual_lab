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
        self.row_name = "main_row_fin"
        self.__render_simulation()
    

    def __render_simulation(self):
        w, h = dpg.get_item_rect_size(self.parent)
        with dpg.table(header_row=False, parent=self.parent):
            dpg.add_table_column(width_stretch=True) # Main Content
            dpg.add_table_column(width_fixed=True, init_width_or_weight=300) # Sidebar
            with dpg.table_row(tag=self.row_name):
                canvas = FinCanvas(self.row_name, w-350, h-50, 0, 0)
                canvas.setup_canvas()
                FinAccordionView(-1, self.row_name, canvas).show_options()
            
            

