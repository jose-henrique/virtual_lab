import dearpygui.dearpygui as dpg

from view.base_analysis_view import BaseAnalysisView
from view.analysis_views.conduction_accordion_view import ConductionAccordionView
from view.canvas.conduction_canvas import ConductionCanvas


class ConductionSimulationView(BaseAnalysisView):
    def __init__(self, parent, width, height, analyze_id):
        self.parent = parent
        self.row_name = f"conduction_row_{id(self)}"
        self.table = f"conduction_table_{id(self)}"
        parent_width, parent_height = dpg.get_item_rect_size(parent)
        self.canvas = ConductionCanvas(
            self.row_name,
            max(1, parent_width - 320),
            max(1, parent_height - 50),
            0,
            0,
        )
        self.options = ConductionAccordionView(self.row_name, self.canvas, analyze_id)

        dpg.add_table(parent=parent, header_row=False, show=False, tag=self.table)
        dpg.add_table_column(width_stretch=True, parent=self.table)
        dpg.add_table_column(width_fixed=True, init_width_or_weight=300, parent=self.table)
        with dpg.table_row(tag=self.row_name, parent=self.table):
            self.canvas.setup_canvas()
            self.options.render()
            self.options.show_options()

    def show_view(self):
        dpg.show_item(self.table)

    def hide_view(self):
        dpg.hide_item(self.table)

    def run_analyze(self):
        self.options.process_results()

    def get_canva(self):
        return self.canvas

    def get_form_data(self):
        return self.options.get_raw_values()

    def set_form_data(self, data):
        self.options.set_raw_values(data)