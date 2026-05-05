import dearpygui.dearpygui as dpg
from gettext import gettext as _
import uuid
from view.data_results.comparison_window_view import ComparisonWindowView
from view.data_results.data_chart_view import DataChartView

class DataResultsView:

    def __init__(self, parent, width, height, analyze_id):
        self.parent = parent
        self.width = width
        self.height = height
        self.height_main_view = height - 500
        self.container_name = f"data_results_container_{uuid.uuid4()}"
        self.comparisonn_window = ComparisonWindowView(self.height_main_view)
        self.data_chart_view = DataChartView(self.height_main_view)
        w, h = dpg.get_item_rect_size(self.parent)
        self.row_name = f"main_row_fin_{uuid.uuid4()}"
        self.scond_row = f"table_row_fin_{uuid.uuid4()}"
        self.__render_simulation()
    

    def __render_simulation(self):
        with dpg.group(parent=self.parent, tag=self.container_name, show=False):
            self.__header_view()
            with dpg.table(header_row=False, parent=self.container_name, show=True) as self.table_id:
                dpg.add_table_column(parent=self.table_id)
                dpg.add_table_column(parent=self.table_id)
                with dpg.table_row(tag=self.row_name, parent=self.table_id):
                    self.comparisonn_window.base_window()
                    self.data_chart_view.base_window()
                with dpg.table_row(tag=self.scond_row, parent=self.table_id):
                    dpg.add_text("some_text")
                
    def __header_view(self):
        dpg.add_text(_("ANALYSIS RESULTS"), parent=self.container_name)
        with dpg.group(horizontal=True, parent=self.container_name):
            dpg.add_text(_("COMPARATIVE THERMAL MODELING"))
            dpg.add_combo([_("Circle"), _("Rectangle")], default_value=_("Filter by Analyze"), tag="filter", width=120)
            dpg.add_button(label=_("\uf04b CLEAR ALL"), tag="button_clear_results", width=120)
            dpg.add_button(label=_("\uf04b SAVE REPORT"), tag="button_save_results", width=120)
            

    def show_view(self):
        self.comparisonn_window.define_analyze_options()
        dpg.configure_item(self.container_name, show=True)

    def hide_view(self):
        dpg.configure_item(self.container_name, show=False)
            
            

