from model.fin_solver import FinSolver
from model.analyze_state_model import state_model
from model.analyze_model import AnalyzeModel


class FinAnalysesController:
    def __init__(self):
        pass
    
    def solve_analyses(self, params, analyze_id):
        solver = FinSolver(params["fin_geometry"], params["solver_method"])
        data = self.__clean_data(params["data"])
        temp_array = solver.find_local_temperature(solver.find_temp_distribuition(data), data.get("env_temperature"), data.get("base_temperature"))
        
        
        temp_distribuition = solver.find_temp_distribuition(data)
        if temp_distribuition:
            self.__save_results({"data": data, "fin_geometry": params["fin_geometry"], "solver_method": params["solver_method"]}, {"temperatures": temp_array, "temp_distribuition": temp_distribuition}, analyze_id)
            return {'temperatures': temp_array, 'base_temperature': 80, 'status': 0}
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
    