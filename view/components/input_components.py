import dearpygui.dearpygui as dpg
from gettext import gettext as _


class InputComponents:
    def __init__(self):
        with dpg.theme() as self.button_theme:
            with dpg.theme_component(dpg.mvButton):
                # Background Color (RGBA)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100, 255))        # Orange
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 150, 150, 255)) # Lighter Orange
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (50, 50, 50, 255))   # Darker Orange
                
                # Text Color inside the button
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255)) 

        with dpg.theme() as self.input_theme:
            with dpg.theme_component(dpg.mvInputFloat):
                dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, 0.5, 0.5) 
        
        with dpg.theme() as self.text_bg_theme:
            with dpg.theme_component(dpg.mvSelectable):
                # This is your "Background Color"
                dpg.add_theme_color(dpg.mvThemeCol_Header, (50, 50, 50, 255))        # Normal state
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (50, 50, 50, 255)) # Hover state
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (50, 50, 50, 255)) 
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))        # Text color (Orange)
                
                # Padding to make it look like a label
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 5)

    def input_float(self, tag, unit, step, label, min_val, max_val,step_fast=0, callback=None, default_val=0, show=True):
        with dpg.group(show=show) as group:
            dpg.add_text(label, color=(150, 150, 150))
            with dpg.group(horizontal=True,horizontal_spacing=0):
                
                def update_val(delta):
                    current = float(dpg.get_value(tag))
                    new_val = max(min_val, min(max_val, current + delta))
                    dpg.set_value(tag, new_val)
                    if callback:
                        callback(tag, new_val, dpg.get_item_user_data(tag))

                m_btn = dpg.add_button(label="-", width=30, callback=lambda: update_val(-step))
                
                dpg.add_input_float(
                    label="",
                    tag=tag,
                    default_value=default_val, 
                    width=100, 
                    step=0,
                    format="%.2f",
                    min_value=min_val,
                    max_value=max_val,
                    min_clamped=True,
                    callback=callback
                )
                
                p_btn = dpg.add_button(label="+", width=30, callback=lambda: update_val(step))
                dpg.add_spacer(width=5)
                #dpg.add_text(unit, color=(100, 100, 100))  
                label = dpg.add_selectable(label=unit, default_value=True, span_columns=False, width=20, height=15) 
        dpg.bind_item_theme(m_btn, self.button_theme)  
        dpg.bind_item_theme(p_btn, self.button_theme)  
        dpg.bind_item_theme(tag, self.input_theme)
        dpg.bind_item_theme(label, self.text_bg_theme)

        return group
    
    def input_int(self, tag, unit, step, label, min_val, max_val,step_fast=0, callback=None, default_val=0, show=True):
            with dpg.group(show=show) as group:
                dpg.add_text(label, color=(150, 150, 150))
                with dpg.group(horizontal=True,horizontal_spacing=0):
                    
                    def update_val(delta):
                        current = int(dpg.get_value(tag))
                        new_val = max(min_val, min(max_val, current + delta))
                        dpg.set_value(tag, new_val)
                        if callback:
                            callback(tag, new_val, dpg.get_item_user_data(tag))

                    m_btn = dpg.add_button(label="-", width=30, callback=lambda: update_val(-step))
                    
                    dpg.add_input_int(
                        label="",
                        tag=tag,
                        default_value=default_val, 
                        width=100, 
                        step=0,
                        min_value=min_val,
                        max_value=max_val,
                        min_clamped=True,
                        callback=callback
                    )
                    
                    p_btn = dpg.add_button(label="+", width=30, callback=lambda: update_val(step))
                    dpg.add_spacer(width=5)
                    #dpg.add_text(unit, color=(100, 100, 100))  
                    label = dpg.add_selectable(label=unit, default_value=True, span_columns=False, width=20, height=15) 
            dpg.bind_item_theme(m_btn, self.button_theme)  
            dpg.bind_item_theme(p_btn, self.button_theme)  
            dpg.bind_item_theme(tag, self.input_theme)
            dpg.bind_item_theme(label, self.text_bg_theme)

            return group

    def slider_float(self, tag, label, default_value=25, show=True):
        slider_theme = self.__set_slider_theme()
        with dpg.group(show=show) as group:
            dpg.add_text(label, color=(150, 150, 150))
            dpg.add_slider_float(label="", default_value=default_value, tag=tag)
        dpg.bind_item_theme(tag, slider_theme)


    def __set_slider_theme(self):
        with dpg.theme() as slider_theme:
            with dpg.theme_component(dpg.mvSliderFloat):
                # 1. The Bar Background
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 43, 50))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 53, 60))
                
                # 2. The "Grab" (The moving handle)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (0, 200, 200)) # Teal
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (0, 255, 255))
                
                # 3. Rounding (Make it look smooth)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 4)
                
                # 4. Thickness
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 6)

        return slider_theme