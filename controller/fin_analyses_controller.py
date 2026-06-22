from model.fin_solver import FinSolver
from model.analyze_state_model import state_model
from model.analyze_model import AnalyzeModel


class FinAnalysesController:
    def __init__(self):
        pass
    
    def solve_analyses(self, params, analyze_id):
        solver = FinSolver(params["fin_geometry"], params["solver_method"])
        data = self.__clean_data(params["data"])
        complete_answers = solver.solve_fin(data)
        temperatures = solver.find_local_temperature(complete_answers["temp_results"], data.get("env_temperature"), data.get("base_temperature"))
        
        
        if complete_answers:
            self.__save_results(
                {"data": data, 
                 "heat_transfer": complete_answers["heat_transfer"],
                 "area": complete_answers["area"],
                 "perimeter": complete_answers["perimeter"],
                 "fin_efficience": complete_answers["fin_efficience"],
                 "fin_geometry": params["fin_geometry"], 
                 "solver_method": params["solver_method"]}, 
                {"temperatures": temperatures}, 
                analyze_id)
            return {'temperatures': temperatures, 'base_temperature': 80, 'status': 0}
        else:
            return {'errors': solver.errors, 'status': -1}
        
        
    def __clean_data(self, data):
        new_data = data
        new_data["dimensions"]["radius"] = data["dimensions"]["radius"]/1000
        new_data["dimensions"]["a"] = data["dimensions"]["a"]/1000
        new_data["dimensions"]["b"] = data["dimensions"]["b"]/1000
        new_data["fin_length"] = data["fin_length"]/1000
        return new_data
    
    def __save_results(self, user_inputs, results, analyze_id):
        analyze_state_model = state_model
        analyze_model = AnalyzeModel()
        analyze = analyze_state_model.get_analyze(analyze_id)
        analyze_model.save_analyze(analyze_id, analyze, user_inputs, results)
    