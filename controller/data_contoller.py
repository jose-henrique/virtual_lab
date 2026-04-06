import dearpygui.dearpygui as dpg
from gettext import gettext as _
from view.error_modal import ErrorModal
from view.success_modal import SuccessModal
from model.analyze_model import AnalyzeModel


class DataController:
    def __init__(self, setup_window):
        self.setup_window = setup_window
        self.error_modal = ErrorModal()
        self.sucess_modal = SuccessModal()
    
    
    def export_data(self, user_inputs, file):
        if not file:
            return
        analyze_data = AnalyzeModel()
        filename = f"{user_inputs.get("location")}/{user_inputs.get("filename")}.csv"
        analyze_data.generate_data_csv(file, filename)
    
    def __success_image_save(self):
        dpg.configure_item(self.setup_window, show=False)
        self.sucess_modal.show_message(_("Image Saved"))
    
    def __error_modal(self, errors):
        self.error_modal.show_errors(errors)  