from gettext import gettext as _
import tempfile
import json
from model.analyze_state_model import state_model
import os
import csv

from model.data_validation import DataValidation

class AnalyzeModel(DataValidation):
    def __init__(self):
        self.errors = []
    
    def get_dataset(self, analyze_id):
        analyze_state_model = state_model
        file = analyze_state_model.avaiable_analyzes[analyze_id].get("file_path")
   
        self.validates("Data", file, validation="presence", message=_("Experiment data not found."))

        if len(self.errors) > 0:
            return False

        return self.__load_data(file)
    
    
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
    
    def __generate_content(self, filedata):
        from model.default_analysis import registry
        spec = registry.get(filedata.get("type"))
        if spec is None:
            raise ValueError(f"No registry found for analyze type: {filedata.get("type")}")

        serializer_cls = spec.serializer_factory
        if serializer_cls is None:
            raise ValueError(f"No serializer found for analyze type: {filedata.get("type")}")

        serializer = serializer_cls()
        return serializer.serialize(filedata)
    
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
            
    def generate_chart_data(self, analyze_a_id, analyze_b_id):
        from model.default_analysis import registry
        experiments = [
            ("experiment_a", "Data a", analyze_a_id, _("Experiment A data not found.")),
            ("experiment_b", "Data b", analyze_b_id, _("Experiment B data not found.")),
        ]

        to_process = []
        for key, label, analyze_id, error_msg in experiments:
            if not analyze_id:
                continue

            file_path = state_model.avaiable_analyzes[analyze_id].get("file_path")
            self.validates(label, file_path, validation="presence", message=error_msg)
            to_process.append((key, file_path))

        if self.errors:
            return False

        results = {}
        for key, file_path in to_process:
            data = self.__load_data(file_path)
            if not isinstance(data, dict):
                continue

            spec = registry.get(data.get("type"))
            if spec is None:
                raise ValueError(f"No registry found for analyze type: {data.get("type")}")

            adapter_cls = spec.chart_adapter_factory
            if adapter_cls is None:
                raise ValueError(f"No adapter found for analyze type: {data.get("type")}")

            adapter = adapter_cls()
            results[key] = adapter.get_chart_data(data)

        return results

    def __remove_previous_file(self, analyze_id):
        analyze_state_model = state_model
        previous_file_path = analyze_state_model.avaiable_analyzes[analyze_id].get("file_path")
        if previous_file_path:
            try:
                os.remove(previous_file_path)
            except OSError as e:
                print(f"Error removing file {previous_file_path}: {e}")

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
            