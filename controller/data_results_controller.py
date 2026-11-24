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

        options = {}
        for analyze_id, analyze in avaiable_analysis.items():
            if analyze.get("type") == "results":
                continue
            if filter is not None and analyze.get("type") != filter:
                continue
            options[analyze.get("name")] = analyze_id

        return options
    
    
    def get_analyze_data(self, experiment_a_id, experiment_b_id, compare_info_view):
        dataset_a = None
        dataset_b = None
        
        if experiment_a_id:
            dataset_a =self.analyze_model.get_dataset(experiment_a_id)
        
        if experiment_b_id:
            dataset_b =self.analyze_model.get_dataset(experiment_b_id)

        if dataset_a or dataset_b:
            compare_info_view.display_analyze_data(dataset_a, dataset_b)
        else:
            self.__error_modal(self.analyze_model.errors)
    
    