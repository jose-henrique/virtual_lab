import dearpygui.dearpygui as dpg
from gettext import gettext as _
import uuid
from view.data_results.comparison_window_view import ComparisonWindowView
from view.data_results.data_chart_view import DataChartView
from model.utils.font_manager import FontManager


class DatasetView:
    def __init__(self, width, height, parent):
        self.width = width
        self.height = height
        self.parent = parent
        self.text_font = FontManager().get("text_roboto_regular_medium")
    
    
    def display_analyze_data(self, dataset_a, dataset_b):
        
        if dpg.does_item_exist("dataset_info_a"):
            dpg.delete_item("dataset_info_a")
            
        if dpg.does_item_exist("dataset_info_b"):
            dpg.delete_item("dataset_info_b")
        
        with dpg.group(tag="dataset_info_a", parent=self.parent):
            self.__dataset_info(dataset_a, 1)
            self.__create_dataset(dataset_a, self.width/2,self.height/4)
            
        with dpg.group(tag="dataset_info_b", parent=self.parent):
            self.__dataset_info(dataset_b, 2)
            self.__create_dataset(dataset_b, self.width/2,self.height/4)
                            
    
    
    def __dataset_info(self, dataset, id):
        dataset_analyze_data = dataset.get("analyze_data")
        dataset_data = dataset_analyze_data.get("data")
        with dpg.group(tag=f"group_info_{id}"):
            
            with dpg.table(header_row=False, resizable=False):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()     
                
                   
                with dpg.table_row():
                    with dpg.group():
                        dpg.add_text(_("Base Temperature"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{dataset_data.get("base_temperature")} °C", color=(124, 246, 236))
                    
                    with dpg.group():
                        dpg.add_text(_("Enviroment Temperature"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{dataset_data.get("env_temperature")} °C", color=(124, 246, 236))
                    
                    with dpg.group():
                        dpg.add_text(_("Material"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{dataset_data.get("fin_material")}", color=(124, 246, 236))
                        
                with dpg.table_row():
                    with dpg.group():
                        dpg.add_text(_("Method"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{self.__solve_method(dataset_analyze_data.get("solver_method"))}", color=(124, 246, 236))
                    
                    with dpg.group():
                        dpg.add_text(_("Area"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{(dataset_analyze_data.get("area")*1000000):.2f} mm²", color=(124, 246, 236))
                    
                    with dpg.group():
                        dpg.add_text(_("Length"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{(dataset_data.get("fin_length")*1000):.2f} mm", color=(124, 246, 236))
                        
                with dpg.table_row():
                    with dpg.group():
                        dpg.add_text(_("Convection Coefficient"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{dataset_data.get("convection_coefficient")} kW/m².K", color=(124, 246, 236))
                    
                    with dpg.group():
                        dpg.add_text(_("Heat"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{dataset_analyze_data.get("heat_transfer"):.2f} W", color=(124, 246, 236))
                    
                    with dpg.group():
                        dpg.add_text(_("Efficience"), wrap=0, color=(190, 91, 16))
                        dpg.add_text(f"{(dataset_analyze_data.get("fin_efficience")*100):.2f} %", color=(124, 246, 236))
            
        
        dpg.bind_item_font(f"group_info_{id}", self.text_font)

                            
                            

    
    def __create_dataset(self, dataset, width, height):
        results = dataset["results"]["temperatures"]
        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True, scrollY=True, borders_innerV=True, borders_outerV=True, width=width, height=height):
                dpg.add_table_column(label="#")
                dpg.add_table_column(label=_("Point"))
                dpg.add_table_column(label=_("Relative Length"))
                dpg.add_table_column(label=_("Temperature Distribuiton (Theta)"))
                dpg.add_table_column(label=_("Local Temperature"))
                
                for idx, row in enumerate(results):
                    with dpg.table_row():
                        dpg.add_text(idx)
                        dpg.add_text(f"{row["point"]:.4f}")
                        dpg.add_text(f"{row["relative_length"]:.4f}")
                        dpg.add_text(f"{row["temp_distribuition"]:.4f}")
                        dpg.add_text(f"{row["local_temp"]:.4f}")
        
    def __solve_method(self, code):
        if code == 1:
            return _("Infinity Fin")
        elif code == 2:
            return _("Adiabatic Fin")
        elif code == 3:
            return _("Specified Temperature")
        elif code == 4:
            return _("Specified Convection")
        


