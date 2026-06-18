from model.analyze_state_model import state_model

from gettext import gettext as _

from view.error_modal import ErrorModal
from model.analyze_model import AnalyzeModel

class DataResultsController:
    
    def __init__(self, view):
        self.comparison_window = view
        self.state_model = state_model
        self.error_modal = ErrorModal()
        self.analyze_model = AnalyzeModel()
        
    def define_aviable_options(self, filter=None):
        avaiable_analysis = self.state_model.get_avaiable_analyzes()
        filtered_analyzes = [analyze for analyze in avaiable_analysis.values() if analyze['type'] == filter] if filter is not None else avaiable_analysis
        
        options = {}
        if not filtered_analyzes:
            return []
        for k, v in avaiable_analysis.items():
            if v.get("type") == "results":
                continue
            options[v.get("name")] = k

        return options
    
    
    def get_analyze_data(self, experiment_a_id, experiment_b_id, compare_info_view):
        dataset_a =self.analyze_model.get_data_set(experiment_a_id)
        dataset_b =self.analyze_model.get_data_set(experiment_b_id)

        if dataset_a and dataset_b:
            compare_info_view.display_analyze_data(dataset_a, dataset_b)
        else:
            self.__error_modal(self.analyze_model.errors)
    
    