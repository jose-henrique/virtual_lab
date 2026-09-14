class AnalysisRegistry:
    def __init__(self):
        self._analysis = {}
        
    def register(self, spec):
        self._analysis[spec.analysis_id] = spec
        
    def get(self, analysis_id):
        return self._analysis.get(analysis_id)
    
    def all(self):
        return self._analysis.values()