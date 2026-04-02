from gettext import gettext as _
import tempfile
import json
from model.analyze_state_model import state_model
import os

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
            "new_cconvection_analyze": {
                "label": _("\uf773 CONVECTION"), 
                "button": _("CONVECTION ANALYZE"), 
                "tag": "convection"
                }
        }

    def get_analyze_options(self):
        return self.analyze_options
    
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