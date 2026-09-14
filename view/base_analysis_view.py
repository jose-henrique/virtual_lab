class BaseAnalysisView:
    def show_view(self):
        raise NotImplementedError
    
    def hide_view(self):
        raise NotImplementedError
    
    def run_analyze(self):
        raise NotImplementedError
    
    def get_form_data(self):
        raise NotImplementedError
    
    def set_form_data(self, data):
        raise NotImplementedError