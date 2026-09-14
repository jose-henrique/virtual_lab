from gettext import gettext as _

class FinSerializer:
    def __init__(self):
        pass
    
    def serialize(self, data):
        content_data = [
                        [_('Analyze Data')],
                    ]
        pre_analyze_data = data.get("analyze_data")
        analyze_data = data.get("analyze_data").get("data")
        results = data.get("results").get("temperatures")
        content_data.append(["Analyze Type", "Fin Analysis"])
        content_data.append([_("Base Temperature (°C)"), analyze_data.get("base_temperature")])        
        content_data.append([_("Enviroment Base Temperature (°C)"), analyze_data.get("env_temperature")])        
        content_data.append([_("End Fin Temperature (°C)"), analyze_data.get("temp_end_fin")])   
        content_data.append([_("Radius (m)"), analyze_data.get("dimensions").get("radius")])   
        content_data.append([_("A (m)"), analyze_data.get("dimensions").get("a")])   
        content_data.append([_("B (m)"), analyze_data.get("dimensions").get("b")])   
        content_data.append([_("Length (m)"), analyze_data.get("fin_length")])   
        content_data.append([_("Convection Coefficient (kW/m²)"), analyze_data.get("convection_coefficient")])   
        content_data.append([_("Material"), analyze_data.get("fin_material")])      
        content_data.append([_("Solve Method"), self.__solve_method(pre_analyze_data.get("solver_method"))]) 
        content_data.append([_("Heat Transfer (W)"), pre_analyze_data.get("heat_transfer")])    
        content_data.append([_("Area (m²)"), pre_analyze_data.get("area")])    
        content_data.append([_("Efficience"), pre_analyze_data.get("fin_efficience")])        
        content_data.append([])
        content_data.append([_("Point (m)"),_("Relative Length ()"), _("Temperature Distribuition ()"), _("Local Temperature (°C)")])
        for result in results:
            content_data.append([result.get("point"), result.get("relative_length"), result.get("temp_distribuition"), result.get("local_temp")])  
        
        return content_data     
    
    def __solve_method(self, code):
            if code == 1:
                return _("Infinity Fin")
            elif code == 2:
                return _("Adiabatic Fin")
            elif code == 3:
                return _("Specified Temperature")
            elif code == 4:
                return _("Specified Convection")