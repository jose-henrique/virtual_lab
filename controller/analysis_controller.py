from view.select_analyze import SelectAnalyze
import uuid
from model.analyze_model import AnalyzeModel
from model.analyze_state_model import state_model
from view.analysis_views.fin_simulation_view import FinSimluationView
from view.data_results.data_results_view import DataResultsView
import copy

class AnalysisController:
    def __init__(self):
        self.analyze_model = AnalyzeModel()
        self.analyze_state_model = state_model

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

    def clone_analyze(self, analyze_id, sidebar):
        analyze_source = self.analyze_state_model.get_analyze(analyze_id)
        if analyze_source is not None:
            analyze_type = analyze_source.get("type")
            analyze = self.analyze_model.get_analyze_options().get(analyze_type)
            analyze_number = self.analyze_state_model.current_analyze_number(analyze_type) + 1
            new_analyze_id = f"{analyze.get("tag")}_{uuid.uuid4()}"
            
            sidebar.add_analyze(f"{analyze.get('label')} {analyze_number}", f"{new_analyze_id}", analyze_type)
            
            source_view = analyze_source.get("view")
            captured_data = source_view.get_form_data() if hasattr(source_view, "get_form_data")  else None
            
            self.analyze_state_model.add_analyze(new_analyze_id, 
                                                 {"type": analyze_type, 
                                                  "view": None, 
                                                  "cloned_data": captured_data,
                                                  "active": False, 
                                                  "analyze_number": analyze_number, 
                                                  "name": self.__define_analyze_name(analyze_type, analyze_number)})
            

    def change_active_analyze(self, analyze_id, analyze_type, size, container):
        analyze_data = self.analyze_state_model.get_avaiable_analyzes().get(analyze_id)
        if analyze_data is None or analyze_data.get("view") is None:
            analyze_number = self.analyze_state_model.current_analyze_number(analyze_type) + 1 if analyze_data is None else analyze_data.get("analyze_number")
            analyze_view = self.__create_analyze_view(analyze_type, size, container, analyze_id)
            
            if analyze_data and ("cloned_data" in analyze_data) and analyze_data["cloned_data"]:
                analyze_view.set_form_data(analyze_data["cloned_data"])
            
            self.analyze_state_model.add_analyze(analyze_id, 
                                                 {"type": analyze_type, 
                                                  "view": analyze_view, 
                                                  "active": True, 
                                                  "analyze_number": analyze_number, 
                                                  "name": self.__define_analyze_name(analyze_type, analyze_number)})
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
        elif analyze_type == "results":
            return DataResultsView(container, w, h, analyze_id)
        
    def __define_analyze_name(self, analyze_type, analyze_number):
        analyze_model = self.analyze_model.get_analyze_options().get(analyze_type)
        if analyze_model is None:
            return f"{analyze_type} {analyze_number}"
        
        return f"{analyze_model.get('tag')} {analyze_number}"