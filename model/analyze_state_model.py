class AnalyzeStateModel:
    _instance = None
    # def __init__(self):
    #     self.active_analyze = None
    #     self.avaiable_analyzes = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalyzeStateModel, cls).__new__(cls)
            cls._instance.active_analyze = None
            cls._instance.avaiable_analyzes = {}
        return cls._instance

    def get_avaiable_analyzes(self):
        return self.avaiable_analyzes
    
    def get_analyze(self, analyze_id):
        return self.avaiable_analyzes.get(analyze_id)
    
    def set_active_analyze(self, analyze):
        self.active_analyze = analyze

    def get_active_analyze(self):
        if self.active_analyze is None:
            return None
        return self.avaiable_analyzes[self.active_analyze]
    
    def add_analyze(self, analyze_id, analyze_data):
        self.avaiable_analyzes[analyze_id] = analyze_data

    def current_analyze_number(self, analyze_type):
        return len([analyze for analyze in self.avaiable_analyzes.values() if analyze.get("type") == analyze_type])