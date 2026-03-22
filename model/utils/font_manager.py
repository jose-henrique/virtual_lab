import dearpygui.dearpygui as dpg   
from pathlib import Path

class FontManager:
    _instance = None
    fonts = {}
    target_sizes = [{"name": "small", "size": 10}, {"name": "base", "size": 15}, {"name": "medium", "size": 24}, {"name": "large", "size": 28}]


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontManager, cls).__new__(cls)
        return cls._instance
    

    def load_all_fonts(self):
        root = Path(__file__).resolve().parents[2]
        fonts_dir = root / "fonts"
        with dpg.font_registry():
            for font_file in fonts_dir.rglob("*"):
                try:
                    extension = font_file.suffix.lower()

                    if extension == ".otf":
                        self.__add_icons_font(font_file)
                    
                    if extension == ".ttf":
                        self.__add_text_font(font_file)
                    
                    
                except Exception as e:
                    print(f"Failed to load {font_file}: {e}")  
                    
    def get(self, name):
        return self.fonts.get(name)
    
    def __add_icons_font(self, font_file):
        file_name = font_file.stem
        suffix = file_name.split("-")[-1]
        self.__generate_size_variation(f"icons_{suffix}", font_file, icon=True)
        
    def __add_text_font(self, font_file):
        file_name = font_file.stem
        prefix = file_name.split("-")[0].lower()
        font_class = file_name.split("-")[1].lower()
        self.__generate_size_variation(f"text_{prefix}_{font_class}", font_file)
    
    
    def __generate_size_variation(self, prefix, font_file, icon=False):
        for size_info in self.target_sizes:
            font_nickname = f"{prefix}_{size_info["name"]}"
            font_id = dpg.add_font(str(font_file), size_info["size"])
            
            if icon:
                dpg.add_font_range(0xf000, 0xf900, parent=font_id)
            
            self.fonts[font_nickname] = font_id
        

    