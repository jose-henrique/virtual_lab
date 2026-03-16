import dearpygui.dearpygui as dpg

class GraphicHandler:
    def __init__(self):
        self.command_set = {}
        self.current_frame = 0
        
    def start_frame(self):
        self.current_frame += 1
        
    def end_frame(self):
        keys_to_delete =[
            tag for tag, command in self.command_set.items()
            if command.get("frame") != self.current_frame and command.get("current_only")
        ]
        
        for tag in keys_to_delete:
            del self.command_set[tag]
    

    def draw_text(self, pos, content, record = True, current_only = False, **kwargs):
        dpg.draw_text(pos, content, **kwargs)
        if not record:
            return
        command_data = {
            "object_type": "text", 
            "content": content, 
            "pos": pos, 
            "size": kwargs.get("size"), 
            "color": kwargs.get("color"),
            "tag": kwargs.get("tag"),
            "current_only": current_only
            }
        self.__update_command_set(command_data) 
    
    def draw_line(self, point_1, point_2, record = True, current_only = False, **kwargs):
        dpg.draw_line(point_1, point_2, **kwargs)
        if not record:
            return
        command_data = {
            "object_type": "line", 
            "point_1": point_1, 
            "point_2": point_2, 
            "color": kwargs.get("color"),
            "tag": kwargs.get("tag"),
            "current_only": current_only
            }
        self.__update_command_set(command_data)
    
    def draw_rectangle(self, point_1, point_2, record = True, current_only = False, **kwargs):
        dpg.draw_rectangle(point_1, point_2, **kwargs)
        if not record:
            return
        command_data = {
            "object_type": "rectangle", 
            "point_1": point_1, 
            "point_2": point_2, 
            "color": kwargs.get("color"), 
            "fill": kwargs.get("fill"),
            "tag": kwargs.get("tag"),
            "current_only": current_only
            }
        self.__update_command_set(command_data)
        
        
    def __update_command_set(self, data):
        tag = data.get("tag")
        data["frame"] = self.current_frame
        if tag:
            self.command_set[tag] = data
        else:
            unique_id = len(self.command_set)
            self.command_set[f"unnamed_{unique_id}"] = data
        