import dearpygui.dearpygui as dpg   
import os

class FontManager:
    _instance = None
    fonts = {}


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontManager, cls).__new__(cls)
        return cls._instance
    

    def load_all_fonts(self):
        root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        for subdir, dirs, files in os.walk(os.path.join(root,"fonts")):
            for file in files:
                print('Loading font: ', file)


fm = FontManager()
fm.load_all_fonts()