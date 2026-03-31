from view.select_analyze import SelectAnalyze
import uuid
from model.analyze_model import AnalyzeModel
from model.analyze_state_model import AnalyzeStateModel
from view.analysis_views.fin_simulation_view import FinSimluationView

class AnalysisController:
    def __init__(self):
        self.analyze_model = AnalyzeModel()
        self.analyze_state_model = AnalyzeStateModel()

    def current_analyze(self):
        return self.analyze_state_model.get_active_analyze()


    def open_new_analysis_modal(self, sender, app_data, user_data):
        sidebar = user_data
        self.select_analyze = SelectAnalyze(sidebar, self.analyze_model.get_analyze_options(), self)
        self.select_analyze.render_modal()

    def add_new_analyse(self, sidebar, analyze_type):
        analyze = self.analyze_model.get_analyze_options().get(analyze_type)
        analyze_number = self.analyze_state_model.current_analyze_number(analyze_type) + 1
        sidebar.add_analyze(f"{analyze.get('label')} {analyze_number}", f"{analyze.get('tag')}_{uuid.uuid4()}", analyze_type)

    def change_active_analyze(self, analyze_id, analyze_type, size, container):
        if self.analyze_state_model.get_avaiable_analyzes().get(analyze_id) is None:
            analyze = self.__create_analyze_view(analyze_type, size, container, analyze_id)
            self.analyze_state_model.add_analyze(analyze_id, {"type": analyze_type, "view": analyze, "active": True})
            self.analyze_state_model.set_active_analyze(analyze_id)
        else:
            self.analyze_state_model.set_active_analyze(analyze_id)
        
        self.__update_screen()

    def run_analyze(self):
        active_analyze = self.analyze_state_model.get_active_analyze()
        if active_analyze is not None:
            active_analyze["view"].run_analyze()           

    def __update_screen(self):
        for analyze_id, analyze_data in self.analyze_state_model.get_avaiable_analyzes().items():
            if analyze_id == self.analyze_state_model.active_analyze:
                analyze_data.get("view").show_view()
            else:
                analyze_data.get("view").hide_view()


    def __create_analyze_view(self, analyze_type, size, container, analyze_id):
        w, h = size
        if analyze_type == "new_fin_analyze":
            return FinSimluationView(container, w, h, analyze_id)