import dearpygui.dearpygui as dpg
from gettext import gettext as _

def save_callback():
    print("Save Clicked")
    
class HomeView:
    def __init__(self):
        with dpg.window(label=_("Window Exemple")):
            dpg.add_text("Hello world")
            dpg.add_button(label="Save", callback=save_callback)
            dpg.add_input_text(label="string")
            dpg.add_slider_float(label="float")