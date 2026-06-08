from model.analyze_state_model import state_model

class DataResultsController:
    
    def __init__(self, view):
        self.comparison_window = view
        self.state_model = state_model
        
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
    
    