from gettext import gettext as _

from view.error_modal import ErrorModal
from model.analyze_model import AnalyzeModel

class ChartsController:
    def __init__(self, data_chart):
        self.data_chart = data_chart
        self.error_modal = ErrorModal()
        self.analyze_model = AnalyzeModel()
    
    def generate_data_chart(self, experiment_a_id, experiment_b_id):
        if experiment_b_id is None or experiment_a_id is None:
            self.__error_modal([_("Please select two experiments to compare.")])
            return
        self.analyze_model.generate_chart_data(experiment_a_id, experiment_b_id)
    
    def __error_modal(self, errors):
        self.error_modal.show_errors(errors)  