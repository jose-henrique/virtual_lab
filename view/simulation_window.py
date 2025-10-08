import dearpygui.dearpygui as dpg
from gettext import gettext as _

class SimulationWindow:
    def __init__(self):
        pass
    
    def base_window(self):
        window_name = "simulation_window"
        if dpg.does_item_exist(window_name):
            dpg.configure_item(window_name, show=True)
        else:
            with dpg.window(label=_("Simulation Window"), 
            tag=window_name,
            width=800,
            height=400,
            pos=[200,200]):
                self.__accordion_options_simulation(window_name)
                
    
    def __accordion_options_simulation(self,parent):
        with dpg.child_window(tag="accordion_simulation",
            width=300,
            autosize_y=True,
            always_use_window_padding=True,
            pos=[0,20],
            parent=parent):
                with dpg.collapsing_header(label=_("Analyse Type"), default_open=True):
                    dpg.add_combo([_("Fins"), _("Forced Convection"), _("Natural Convection"), _("Conduction"), _("Heat Changer")])
                with dpg.collapsing_header(label=_("Geometry"), default_open=True):
                    dpg.add_combo([_("Circle"), _("Rectangle")])
                    dpg.add_text(_("Radius"))
                    dpg.add_input_text(no_spaces=True, auto_select_all=True)
                    dpg.add_text(_("Length"))
                    dpg.add_input_text(no_spaces=True, auto_select_all=True)
                    dpg.add_text(_("Convection Coeficienty"))
                    dpg.add_input_text(no_spaces=True, auto_select_all=True)
                with dpg.collapsing_header(label=_("Physical Properties"), default_open=True):
                    dpg.add_text("Simulation Content Here")
                with dpg.collapsing_header(label=_("Enviroment"), default_open=True):
                    dpg.add_text("Simulation Content Here")
                with dpg.collapsing_header(label=_("Run Simulation"), default_open=True):
                    dpg.add_text("Simulation Content Here")