import dearpygui.dearpygui as dpg
from gettext import gettext as _
from view.error_modal import ErrorModal
import time


class ExperimentsOptionsMasterView:
    
    def __init__(self):
        self.view_name = ""
        self.unique_id = str(int(time.time()))
        self.pos = [0,90]
        
    def process_results(self):
        pass
    
    def show_options(self):
        dpg.show_item(self.view_name)
    
    def hide_options(self):
        dpg.hide_item(self.view_name)
        
    def error_callback(self, errors):
        error_modal = ErrorModal()
        error_modal.show_errors(errors)    
        