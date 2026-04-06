from gettext import gettext as _
import tempfile
import json
from model.analyze_state_model import state_model
import os
import csv

class AnalyzeModel:
    def __init__(self):
        self.analyze_options = {
            "new_fin_analyze": {
                "label": _("\uf2c8 FIN"), 
                "button": _("FIN ANALYZE"), 
                "tag": "fin"
                }, 
            "new_conduction_analyze": {
                "label": _("\uf029 CONDUCTION"), 
                "button": _("CONDUCTION ANALYZE"), 
                "tag": "conduction"
                },
            "new_convection_analyze": {
                "label": _("\uf773 CONVECTION"), 
                "button": _("CONVECTION ANALYZE"), 
                "tag": "convection"
                }
        }

    def get_analyze_options(self):
        return self.analyze_options
    

    def generate_data_csv(self, file, filename):
        try:
            saved_data = self.__load_data(file)
            data = self.__generate_content(saved_data)
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            
            return 0    
        except Exception as e:
            print(f"Failed with error: {e}")
            return -1
    
    def save_analyze(self, analyze_id, analyze, analyze_data, results):
        analyze_state_model = state_model
        self.__remove_previous_file(analyze_id)
        data = {
            "analyze_number": analyze.get("analyze_number"),
            "analyze_id": analyze_id,
            "type": analyze.get("type"),
            "analyze_data": analyze_data,
            "results": results
        }

        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_file:
            json.dump(data, temp_file)
            temp_file.seek(0)
            analyze_state_model.avaiable_analyzes[analyze_id]["file_path"] = temp_file.name
            print(f"Analyze data saved to {temp_file.name}")

    
    def __remove_previous_file(self, analyze_id):
        analyze_state_model = state_model
        previous_file_path = analyze_state_model.avaiable_analyzes[analyze_id].get("file_path")
        if previous_file_path:
            try:
                os.remove(previous_file_path)
            except OSError as e:
                print(f"Error removing file {previous_file_path}: {e}")
                

    def __generate_content(self, filedata):
        data = [
                [_('Analyze Data')],
            ]
        if filedata.get("type") == "new_fin_analyze":
            analyze_type = self.analyze_options.get(filedata.get("type")).get("button")
            analyze_data = filedata.get("analyze_data")
            results = filedata.get("results").get("temperatures")
            data.append(["Analyze Type", analyze_type])
            data.append([_("Base Temperature (°C)"), analyze_data.get("base_temperature")])        
            data.append([_("Enviroment Base Temperature (°C)"), analyze_data.get("env_temperature")])        
            data.append([_("End Fin Temperature (°C)"), analyze_data.get("temp_end_fin")])   
            data.append([_("Radius (m)"), analyze_data.get("dimension").get("radius")])   
            data.append([_("A (m)"), analyze_data.get("dimension").get("a")])   
            data.append([_("B (m)"), analyze_data.get("dimension").get("b")])   
            data.append([_("Length (m)"), analyze_data.get("fin_length")])   
            data.append([_("Material"), analyze_data.get("fin_material")])   
            data.append([_("Conduction Coefficient")])   
            data.append([_("Solve Method")]) 
            data.append([])
            data.append([_("Point (m)"),_("Temperature Distribuition ()"),_("Temperature Distribuition ()"), _("Local Temperature (°C)")])
            for result in results:
                data.append([result.get("point"), result.get("temp_distribuition"), result.get("local_temp")])  
            
            return data     

    def __load_data(self,file):
        try:
            with open(file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: The file {file} was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {file}.")
        return None