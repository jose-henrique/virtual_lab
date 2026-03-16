import dearpygui.dearpygui as dpg
from model.utils.image_handler import ImageHandler
from model.utils.graphic_handler import GraphicHandler

class CanvaHandler:
    def __init__(self,parent, width, height, offset_x,offset_y):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.parent = parent
        self.graphic_handler = GraphicHandler()
    
    
    def setup_canvas(self):
        window_width = dpg.get_item_width(self.parent)
        self.width = (window_width - self.offset_x)
        with dpg.group(pos=[self.offset_x, self.offset_y], parent=self.parent):
            with dpg.drawlist(width=self.width, height=self.height, tag=self.name):
                self._initial_draw()
    
    def _initial_draw(self):
        pass
            
    def save_image(self, user_inputs):
        image_handler = ImageHandler(
            self.graphic_handler.command_set,
            self.width, self.height, 
            (self.width - (self.fin_width + 20))/2, 
            width=user_inputs["image_size"][0], 
            height=user_inputs["image_size"][1],
            location=user_inputs["location"],
            filename=user_inputs["filename"],
            background_color=user_inputs["background_color"]
            )
        return image_handler.generate_and_save()
        