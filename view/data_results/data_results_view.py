import dearpygui.dearpygui as dpg
from gettext import gettext as _
import uuid
from view.data_results.comparison_window_view import ComparisonWindowView
from view.data_results.data_chart_view import DataChartView
from model.utils.font_manager import FontManager
from view.data_results.dataset_view import DatasetView

class DataResultsView:

    def __init__(self, parent, width, height, analyze_id, analyze_options):
        self.parent = parent
        self.width = width
        self.height = height
        self.height_main_view = height - 500
        self.analyze_options = self.__define_options(analyze_options)
        self.container_name = f"data_results_container_{uuid.uuid4()}"
        self.row_name = f"main_row_fin_{uuid.uuid4()}"
        self.scond_row = f"table_row_fin_{uuid.uuid4()}"
        self.dataset_view = DatasetView(width, height, self.scond_row )
        self.data_chart_view = DataChartView(self.height_main_view)
        self.comparisonn_window = ComparisonWindowView(self.height_main_view, self.data_chart_view, self.dataset_view)
        self.icons_font = FontManager().get("icons_solid_small")
        self.text_font = FontManager().get("text_roboto_regular_medium")
        w, h = dpg.get_item_rect_size(self.parent)
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
                    pass
                
    def __header_view(self):
        dpg.add_text(_("ANALYSIS RESULTS"), parent=self.container_name, tag="header_title_results")
        with dpg.group(horizontal=True, parent=self.container_name, tag="results_options"):
            dpg.add_text(_("COMPARATIVE THERMAL MODELING"))
            dpg.add_combo(list(self.analyze_options.keys()), default_value=_("Filter by Analyze"), tag="filter", width=150, callback=self.__filter_analyses)
            dpg.add_button(label=_("\uf2ed CLEAR ALL"), tag="button_clear_results", width=120, callback=self.__clear_results)
            dpg.add_button(label=_("\uf0c7 SAVE REPORT"), tag="button_save_results", width=120)
        
        
        dpg.bind_item_font("header_title_results", self.text_font)
        dpg.bind_item_font("results_options", self.icons_font)
            

    def show_view(self):
        self.comparisonn_window.define_analyze_options()
        dpg.configure_item(self.container_name, show=True)

    def hide_view(self):
        dpg.configure_item(self.container_name, show=False)
        
        
    def __define_options(self, analyze_options):
        items = {}
        for option, value in analyze_options.items():
            items[f"{value.get("name")}"] = option

        return items
    
    def __clear_results(self, sender, app_data, user_data):
        self.comparisonn_window.clear_combos()
        self.dataset_view.remove_infos()
        self.data_chart_view.remove_series("a")
        self.data_chart_view.remove_series("b")
    

    
    def __filter_analyses(self, sender, app_data, user_data):
        
        self.comparisonn_window.filter_analyses(self.analyze_options[app_data])
            
            

