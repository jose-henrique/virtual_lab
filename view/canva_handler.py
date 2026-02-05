import dearpygui.dearpygui as dpg
from model.utils import Utils
import matplotlib.cm as cm
import matplotlib.colors as colors

class CanvaHandler:
    def __init__(self,parent, width, height, offset_x,offset_y):
        self.width = width
        self.height = 600#dpg.get_item_height(parent)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.parent = parent
        self.fin_width = 400
        self.fin_height = 60
        self.ref = [self.offset_x, self.offset_y]
    
    
    def initial_draw(self):
        ref = [self.offset_x, self.offset_y]
        with dpg.drawlist(width=self.width, height=self.height, parent=self.parent, pos=[0, 0], tag="canva"):
            self.__draw_base(ref)
            self.__draw_fin_profile(ref)
            
    
    def set_base_temp(self, temp):
        dpg.delete_item("base_temperature_label")
        dpg.draw_text([self.offset_x + 40, 350], f"{temp} °C", size=17, color=(255, 255, 255), parent="canva", tag="base_temperature_label")
        
    def set_fin_length(self, legth):
        dpg.delete_item("fin_length_label")
        center_x = (self.second_vertical_bar_pos_x + self.first_vertical_bar_pos_x)/2
        pos_y = self.horzontal_dimension_pos - 20
        dpg.draw_text([center_x - 40, pos_y], f"{legth} mm", size=17, color=(255, 255, 255), parent="canva", tag="fin_length_label")
    
    def set_fin_height(self, legth):
        dpg.delete_item("fin_height_label")
        center_y = (self.second_horizontal_bar_pos_y + self.first_horizontal_bar_pos_y)/2
        pos_x = self.vertical_dimension_pos + 10
        dpg.draw_text([pos_x, center_y - 10], f"{legth} mm", size=17, color=(255, 255, 255), parent="canva", tag="fin_height_label")
        
    def color_fin(self, temp_distribuition_array, base_temperature):
        utils = Utils()
        nodes = len(temp_distribuition_array)
        node_height = self.fin_height
        node_pos_y = self.ref[1] + ((self.height/2)-(node_height/2))
        node_pos_x = self.ref[0] + 69
        node_width = self.fin_width / nodes
        temperatures = [item['local_temp'] for item in temp_distribuition_array]
        normalized = colors.Normalize(vmin=min(temperatures), vmax=max(temperatures))
        cmap = cm.get_cmap('coolwarm')
        
        for element in temp_distribuition_array:
            rgb_color = tuple(int(255 * c) for c in cmap(normalized(element["local_temp"]))[:3])
            dpg.draw_rectangle([node_pos_x, node_pos_y], [(node_pos_x + node_width), (node_pos_y + node_height)], color=(255,255,255), fill=rgb_color, parent="canva")
            node_pos_x += node_width
            

        
        
    def __draw_base(self, ref):
        rect_height = 90
        rect_width = 20
        pos_x_rect = ref[0] + 50
        pos_y_rect = ref[1] + ((self.height/2)-(rect_height/2))
        dpg.draw_rectangle([pos_x_rect, pos_y_rect], [(pos_x_rect + rect_width), (pos_y_rect + rect_height)], color=(255, 255, 255),fill=(230, 0, 0, 255))
    
    def __draw_fin_profile(self, ref):
        rect_height = self.fin_height
        rect_width = self.fin_width
        pos_x_rect = ref[0] + 69
        pos_y_rect = ref[1] + ((self.height/2)-(rect_height/2))
        dpg.draw_rectangle([pos_x_rect, pos_y_rect], [(pos_x_rect + rect_width), (pos_y_rect + rect_height)], color=(255, 255, 255))
        self.__draw_dimensions_lines(ref,pos_x_rect,pos_y_rect,rect_height)
    
    def __draw_dimensions_lines(self, ref, fin_x_position, fin_y_position, fin_height):
        self.first_vertical_bar_pos_x = ref[0] + 69
        self.second_vertical_bar_pos_x = ref[0] + 68 + self.fin_width
        vertical_bar_height = 100
        self.horzontal_dimension_pos = fin_y_position - 80
        horizontal_bars_x = self.second_vertical_bar_pos_x + 30
        horizontal_bars_width = 40
        self.first_horizontal_bar_pos_y = ref[1] + fin_y_position
        self.second_horizontal_bar_pos_y = ref[1] + fin_y_position + fin_height
        self.vertical_dimension_pos = horizontal_bars_x+horizontal_bars_width-20
        
        dpg.draw_line([self.first_vertical_bar_pos_x, (fin_y_position -30)], [self.first_vertical_bar_pos_x, (fin_y_position-vertical_bar_height)], color=(255, 255, 255))
        dpg.draw_line([self.second_vertical_bar_pos_x, (fin_y_position -30)], [self.second_vertical_bar_pos_x, (fin_y_position-vertical_bar_height)], color=(255, 255, 255))
        dpg.draw_line([self.first_vertical_bar_pos_x, self.horzontal_dimension_pos], [self.second_vertical_bar_pos_x, self.horzontal_dimension_pos], color=(255, 255, 255))
        
        dpg.draw_line([horizontal_bars_x, self.first_horizontal_bar_pos_y], [(horizontal_bars_x+horizontal_bars_width), self.first_horizontal_bar_pos_y], color=(255, 255, 255))
        dpg.draw_line([horizontal_bars_x, self.second_horizontal_bar_pos_y], [(horizontal_bars_x+horizontal_bars_width), self.second_horizontal_bar_pos_y], color=(255, 255, 255))
        dpg.draw_line([self.vertical_dimension_pos, self.first_horizontal_bar_pos_y], [self.vertical_dimension_pos, self.second_horizontal_bar_pos_y], color=(255, 255, 255))