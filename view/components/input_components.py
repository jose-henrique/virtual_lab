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

    def input_float(self, tag, unit, step, label, min, max, callback, step_fast, default_val=0):
        with dpg.group():
            dpg.add_text(label, color=(150, 150, 150))
            with dpg.group(horizontal=True,horizontal_spacing=0):
                
                m_btn = dpg.add_button(label="-", width=30, callback=lambda: dpg.set_value(tag, dpg.get_value(tag)-step))
                
                dpg.add_input_float(
                    label="",
                    tag=tag,
                    default_value=default_val, 
                    width=100, 
                    step=0,
                    format="%.2f",
                    min_value=min,
                    max_value=max,
                    min_clamped=True,
                    callback=callback
                )
                
                p_btn = dpg.add_button(label="+", width=30, callback=lambda: dpg.set_value(tag, dpg.get_value(tag)+step))
                dpg.add_spacer(width=5)
                #dpg.add_text(unit, color=(100, 100, 100))  
                label = dpg.add_selectable(label=unit, default_value=True, span_columns=False, width=20, height=15) 
        dpg.bind_item_theme(m_btn, self.button_theme)  
        dpg.bind_item_theme(p_btn, self.button_theme)  
        dpg.bind_item_theme(tag, self.input_theme)
        dpg.bind_item_theme(label, self.text_bg_theme)
    