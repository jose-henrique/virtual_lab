

class AnalyzeStateModel:
    def __init__(self):
        self.active_analyze = None
        self.avaiable_analyzes = {}

    def get_avaiable_analyzes(self):
        return self.avaiable_analyzes
    
    def set_active_analyze(self, analyze):
        self.active_analyze = analyze
    
    def add_analyze(self, analyze_id, analyze_data):
        self.avaiable_analyzes[analyze_id] = analyze_data