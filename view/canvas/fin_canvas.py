import dearpygui.dearpygui as dpg
import matplotlib.cm as cm
import matplotlib.colors as colors
from view.canvas.canva_handler import CanvaHandler
import time

class FinCanvas(CanvaHandler):
    def __init__(self,parent, width, height, offset_x,offset_y):
        self.unique_id = str(int(time.time()))
        self.name = f"fin_canva_{self.unique_id}"
        super().__init__(parent, width, height, offset_x,offset_y)
        self.fin_width = 400
        self.fin_height = 60
        self.base_width = 20
        self.base_height = 90
        self.object_width = self.base_width + self.fin_width
        self.object_height = self.base_height
    
    
    def _initial_draw(self):
        self.__draw_base()
        self.__draw_fin_profile()
        with dpg.draw_layer(tag=f"results_group_{self.unique_id}", parent=self.name):
            pass
    
    def set_base_temp(self, temp):
        dpg.delete_item(f"base_temperature_label_{self.unique_id}")
        self.graphic_handler.draw_text([(self.width -self.object_width)/2, 390], f"{temp} °C", size=17, color=(255, 255, 255), parent=self.name, tag=f"base_temperature_label_{self.unique_id}")
        
    def set_fin_length(self, legth):
        dpg.delete_item(f"fin_length_label_{self.unique_id}")
        center_x = (self.second_vertical_bar_pos_x + self.first_vertical_bar_pos_x)/2
        pos_y = self.horzontal_dimension_pos - 20
        self.graphic_handler.draw_text([center_x - 40, pos_y], f"{legth} mm", size=17, color=(255, 255, 255), parent=self.name, tag=f"fin_length_label_{self.unique_id}")
    
    def set_fin_height(self, legth):
        dpg.delete_item(f"fin_height_label_{self.unique_id}")
        center_y = (self.second_horizontal_bar_pos_y + self.first_horizontal_bar_pos_y)/2
        pos_x = self.vertical_dimension_pos + 10
        self.graphic_handler.draw_text([pos_x, center_y - 10], f"{legth} mm", size=17, color=(255, 255, 255), parent=self.name, tag=f"fin_height_label_{self.unique_id}")
        
    def color_fin(self, temp_distribuition_array, base_temperature):
        self.graphic_handler.start_frame()
        nodes = len(temp_distribuition_array)
        node_height = self.fin_height
        node_pos_y = ((self.height/2)-(node_height/2))
        node_pos_x = ((self.width -self.object_width)/2) + self.base_width
        node_width = self.fin_width / nodes
        temperatures = [item['local_temp'] for item in temp_distribuition_array]
        normalized = colors.Normalize(vmin=min(temperatures), vmax=max(temperatures))
        cmap = cm.get_cmap('coolwarm')
        
        dpg.delete_item(f"results_group_{self.unique_id}", children_only=True)
        for i, element in enumerate(temp_distribuition_array):
            rgb_color = tuple(int(255 * c) for c in cmap(normalized(element["local_temp"]))[:3])
            self.graphic_handler.draw_rectangle([node_pos_x, node_pos_y], [(node_pos_x + node_width), (node_pos_y + node_height)], color=(255,255,255), fill=rgb_color, parent=f"results_group_{self.unique_id}", tag=f"rect_{i}", current_only=True)
            self.__draw_subtitle(i, nodes, element["local_temp"], rgb_color)
            node_pos_x += node_width
        self.graphic_handler.end_frame()
            
    
    def __draw_subtitle(self, idx, nodes, temperature, fill):
        first_subtile_pos_y = 10
        max_height = 340
        node_height = max_height /nodes
        node_width = 30
        posx_x_0 = 20
        posx_x_1 = posx_x_0 + node_width
        current_top_position = first_subtile_pos_y + (node_height*idx)
        step = (nodes - 1) / 4
        targets = {0, round(step), round(step*2), round(step*3), nodes-1}
        self.graphic_handler.draw_rectangle([posx_x_0, current_top_position], [posx_x_1, current_top_position+node_height], color=fill, fill=fill, parent=f"results_group_{self.unique_id}", tag=f"square_title_{idx}", current_only=True)
        if idx in targets:
            self.graphic_handler.draw_text([(posx_x_1 + 5), current_top_position], f"{temperature:.2f} °C", size=17, color=(255, 255, 255), parent=f"results_group_{self.unique_id}", tag=f"temp_title_{idx}", current_only=True)
        
            

    def __draw_base(self):
        pos_x_rect = (self.width - self.object_width)/2
        pos_y_rect = ((self.height/2)-(self.base_height/2))
        self.graphic_handler.draw_rectangle([pos_x_rect, pos_y_rect], [(pos_x_rect + self.base_width), (pos_y_rect + self.base_height)], color=(255, 255, 255),fill=(230, 0, 0, 255))
    
    def __draw_fin_profile(self):
        pos_x_rect = ((self.width -self.object_width)/2) + self.base_width
        pos_y_rect = ((self.height/2)-(self.fin_height/2))
        self.graphic_handler.draw_rectangle([pos_x_rect, pos_y_rect], [(pos_x_rect + self.fin_width), (pos_y_rect + self.fin_height)], color=(255, 255, 255))
        self.__draw_dimensions_lines(pos_x_rect,pos_y_rect,self.fin_height)
    
    def __draw_dimensions_lines(self, fin_x_position, fin_y_position, fin_height):
        self.first_vertical_bar_pos_x = fin_x_position
        self.second_vertical_bar_pos_x = fin_x_position + self.fin_width
        vertical_bar_height = 100
        self.horzontal_dimension_pos = fin_y_position - 80
        horizontal_bars_x = self.second_vertical_bar_pos_x + 30
        horizontal_bars_width = 40
        self.first_horizontal_bar_pos_y = fin_y_position
        self.second_horizontal_bar_pos_y = fin_y_position + fin_height
        self.vertical_dimension_pos = horizontal_bars_x+horizontal_bars_width-20
        
        self.graphic_handler.draw_line([self.first_vertical_bar_pos_x, (fin_y_position -30)], [self.first_vertical_bar_pos_x, (fin_y_position-vertical_bar_height)], color=(255, 255, 255))
        self.graphic_handler.draw_line([self.second_vertical_bar_pos_x, (fin_y_position -30)], [self.second_vertical_bar_pos_x, (fin_y_position-vertical_bar_height)], color=(255, 255, 255))
        self.graphic_handler.draw_line([self.first_vertical_bar_pos_x, self.horzontal_dimension_pos], [self.second_vertical_bar_pos_x, self.horzontal_dimension_pos], color=(255, 255, 255))
        
        self.graphic_handler.draw_line([horizontal_bars_x, self.first_horizontal_bar_pos_y], [(horizontal_bars_x+horizontal_bars_width), self.first_horizontal_bar_pos_y], color=(255, 255, 255))
        self.graphic_handler.draw_line([horizontal_bars_x, self.second_horizontal_bar_pos_y], [(horizontal_bars_x+horizontal_bars_width), self.second_horizontal_bar_pos_y], color=(255, 255, 255))
        self.graphic_handler.draw_line([self.vertical_dimension_pos, self.first_horizontal_bar_pos_y], [self.vertical_dimension_pos, self.second_horizontal_bar_pos_y], color=(255, 255, 255))
        
    
    def __draw_tooltip(self, temperature, idx, x, y, width, height):
        if dpg.does_item_exist(f"rect_btn_{idx}"):
            self.__update_tooltip(idx, temperature)
        else:
            self.__create_tooltip(temperature, idx, x, y, width, height)
        
            
    def __create_tooltip(self, temperature, idx, x, y, width, height):
        dpg.add_button(
                    parent=self.parent,
                    label="", 
                    pos=[x, y], 
                    width=width, 
                    height=height, 
                    tag=f"rect_btn_{idx}"
                )
        with dpg.theme() as invisible_btn_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 255, 255, 20]) # Leve brilho ao passar o mouse
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
                
        dpg.bind_item_theme(f"rect_btn_{idx}", invisible_btn_theme)
        
        with dpg.tooltip(f"rect_btn_{idx}"):
            dpg.add_text(f"Local Temperature: {temperature:.2f}°C", tag=f"tooltip_text_{idx}")
            
    def __update_tooltip(self, idx, temperature):
        dpg.set_value(f"tooltip_text_{idx}", f"Local Temperature: {temperature:.2f}°C")