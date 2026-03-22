import dearpygui.dearpygui as dpg
from model.utils.image_handler import ImageHandler
from model.utils.graphic_handler import GraphicHandler

class CanvaHandler:
    def __init__(self,parent, width, height, offset_x,offset_y):
        self.width = 600
        self.height = 600
        self.offset_x = 0
        self.offset_y = 0
        self.parent = parent
        self.graphic_handler = GraphicHandler()
    
    
    def setup_canvas(self):
        #window_width = dpg.get_item_width(self.parent)
        #self.width = (window_width - self.offset_x)
        #print(dpg.get_item_rect_size(self.parent))
        with dpg.drawlist(width=-1, height=-1, tag=self.name, parent=self.parent):
            w = 600
            h = 600

            # 2. Draw the rectangle using these dimensions
            # We subtract 1 or 2 pixels so the border doesn't get "cut off" by the edge
            dpg.draw_rectangle(
                pmin=[1, 1], 
                pmax=[w - 1, h - 1], 
                color=(255, 140, 65, 255),  # Your Orange Accent
                thickness=2.0,
                parent="canvas" # The tag of your drawlist
            )
            #self._initial_draw()
        #with dpg.group(pos=[self.offset_x, self.offset_y], parent=self.parent):
    
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
        