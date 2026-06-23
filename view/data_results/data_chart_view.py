import dearpygui.dearpygui as dpg
from gettext import gettext as _
import uuid


class DataChartView:
    def __init__(self, height):
        self.window_name = "data_chart_view"
        self.width_window = 300
        self.x_axis = "x_axis"
        self.y_axis = "y_axis"
        self.height_window = height
        self.series_a = "series_a_" + str(uuid.uuid4())
        self.series_b = "series_b_" + str(uuid.uuid4())

    def base_window(self):
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            with dpg.child_window(label=_("DATA CHART"), tag=self.window_name,
            always_use_window_padding=True,
            height= self.height_window,
            show=True):
                with dpg.plot(label=_("Experiment Chart"), width=-1, height=-1):
                    dpg.add_plot_axis(dpg.mvXAxis, label=_("Relative Length ()"), tag=self.x_axis)
                    dpg.add_plot_axis(dpg.mvYAxis, label=_("Temperature (°C)"), tag=self.y_axis)
                    
                    dpg.add_plot_legend()

    def update_chart(self, dataset_a, dataset_b):
        if not dpg.does_item_exist(self.window_name):
            return
        
        if dataset_a:
            self.remove_series("a")
            self.__add_new_series(dataset_a, "a")
        
        if dataset_b:
            self.remove_series("b")
            self.__add_new_series(dataset_b, "b")
        
        dpg.fit_axis_data("y_axis")
        dpg.fit_axis_data("x_axis")
        

    
    def __add_new_series(self, dataset, experiment_code):
        new_tag = f"data_series_{experiment_code}"
        
        dados_x = dataset[0]
        dados_y = dataset[1]
        
        
        dpg.add_line_series(
            x=dados_x, 
            y=dados_y, 
            label=_(f"Experiment {experiment_code}"), 
            parent=self.x_axis,
            tag=new_tag
        )
        
    def remove_series(self, experiment_code):
            tag = f"data_series_{experiment_code}"
            if dpg.does_item_exist(tag):
                dpg.delete_item(tag)

