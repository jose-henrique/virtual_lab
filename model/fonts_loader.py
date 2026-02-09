import dearpygui.dearpygui as dpg
import os

class FontLoader:
    def __init__(self, font_name="", font_size=12):
        self.font_name = font_name
        self.font_size = font_size
        pass

    def load_font(self):
        root_folder = os.path.dirname(os.path.dirname(__file__))
        font_name = self.font_name if self.font_name else "Roboto-Regular.ttf"
        font_path = os.path.join(root_folder,"fonts", font_name)
        with dpg.font_registry():
            with dpg.font(font_path, self.font_size) as loadedFont:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        return loadedFont       