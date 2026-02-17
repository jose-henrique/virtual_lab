import dearpygui.dearpygui as dpg
from gettext import gettext as _
#from controller.charts_controller import ChartsController
from view.error_modal import ErrorModal

class ChartView:
    def __init__(self):
        self.window_name = "chart_window"
        self.width_window = 1000
    
    def base_window(self):
        
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            with dpg.window(label=_("Charts Window"), 
            tag=self.window_name,
            width=self.width_window,
            height=600,
            pos=[200,20]):   
                self.__data_table()
                
    def __data_table(self):
        print("hello")