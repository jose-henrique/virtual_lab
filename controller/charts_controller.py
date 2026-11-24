from gettext import gettext as _

from view.error_modal import ErrorModal
from model.analyze_model import AnalyzeModel

class ChartsController:
    def __init__(self, data_chart):
        self.data_chart = data_chart
        self.error_modal = ErrorModal()
        self.analyze_model = AnalyzeModel()
    
    def generate_data_chart(self, experiment_a_id, experiment_b_id):
        if experiment_b_id is None and experiment_a_id is None:
            self.__error_modal([_("Please select an experiment to plot.")])
            return
        results =self.analyze_model.generate_chart_data(experiment_a_id, experiment_b_id)

        if results:
            self.data_chart.update_chart(
                results.get("experiment_a"),
                results.get("experiment_b"),
                self.__x_axis_label(results.get("x_labels", {})),
            )
        else:
            self.__error_modal(self.analyze_model.errors)
    
    def __x_axis_label(self, x_labels):
        # Each analysis type defines its own X axis; when two different types are compared, show both.
        labels = []
        for key in ("experiment_a", "experiment_b"):
            label = x_labels.get(key)
            if label and label not in labels:
                labels.append(label)
        return " | ".join(_(label) for label in labels)

    def __error_modal(self, errors):
        self.error_modal.show_errors(errors)  