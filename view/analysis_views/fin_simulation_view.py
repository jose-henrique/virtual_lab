import dearpygui.dearpygui as dpg
from gettext import gettext as _
from model.utils.font_manager import FontManager
from view.analysis_views.fin_accordion_view import FinAccordionView
from  view.canvas.fin_canvas import FinCanvas
import uuid

class FinSimluationView:

    def __init__(self, parent, width, height):
        self.parent = parent
        self.width = width
        self.height = height
        w, h = dpg.get_item_rect_size(self.parent)
        self.row_name = f"main_row_fin_{uuid.uuid4()}"
        self.canvas = FinCanvas(self.row_name, w-350, h-50, 0, 0)
        self.fin_accordion_view = FinAccordionView(-1, self.row_name, self.canvas)
        self.__render_simulation()
    

    def __render_simulation(self):
        
        
        with dpg.table(header_row=False, parent=self.parent, show=False) as self.table_id:
            dpg.add_table_column(width_stretch=True, parent=self.table_id) # Main Content
            dpg.add_table_column(width_fixed=True, init_width_or_weight=300, parent=self.table_id) # Sidebar
            with dpg.table_row(tag=self.row_name, parent=self.table_id):
                self.canvas.setup_canvas()
                self.fin_accordion_view.render_accordion()
                self.fin_accordion_view.show_options()

    def show_view(self):
        dpg.configure_item(self.table_id, show=True)

    def hide_view(self):
        dpg.configure_item(self.table_id, show=False)

    def run_analyze(self):
        self.fin_accordion_view.process_results()
            
            

