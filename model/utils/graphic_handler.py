import dearpygui.dearpygui as dpg

class GraphicHandler:
    def __init__(self):
        self.command_set = []
    

    def draw_text(self, pos, content, record = True, **kwargs):
        dpg.draw_text(pos, content, **kwargs)
        if not record:
            return
        command_data = {
            "object_type": "text", 
            "content": content, 
            "pos": pos, 
            "size": kwargs.get("size"), 
            "color": kwargs.get("color")
            }
        self.__update_command_set(command_data) 
    
    def draw_line(self, point_1, point_2, record = True, **kwargs):
        dpg.draw_line(point_1, point_2, **kwargs)
        if not record:
            return
        command_data = {
            "object_type": "line", 
            "point_1": point_1, 
            "point_2": point_2, 
            "color": kwargs.get("color")
            }
        self.__update_command_set(command_data)
    
    def draw_rectangle(self, point_1, point_2, record = True, **kwargs):
        dpg.draw_rectangle(point_1, point_2, **kwargs)
        if not record:
            return
        command_data = {
            "object_type": "rectangle", 
            "point_1": point_1, 
            "point_2": point_2, 
            "color": kwargs.get("color"), 
            "fill": kwargs.get("fill")
            }
        self.__update_command_set(command_data)
        
        
    def __update_command_set(self, data):
        self.command_set.append(data)
            
        