import dearpygui.dearpygui as dpg
from gettext import gettext as _
from view.error_modal import ErrorModal
from view.success_modal import SuccessModal

class ImagesController:
    def __init__(self, canva, setup_window):
        self.canva = canva
        self.setup_window = setup_window
    
    
    def save_image(self, data):
        results = self.canva.save_image(data)
        if results["status"] == 0:
            self.__success_image_save()
        elif results["status"] == -1:
            self.__error_image_save(results["errors"]) 
    
    def __success_image_save(self):
        dpg.configure_item(self.setup_window, show=False)
        SuccessModal().show_message(_("Image Saved"))
    
    def __error_image_save(self, errors):
        error_modal = ErrorModal()
        error_modal.show_errors(errors)      
        
           