from model.fin_solver import FinSolver


class FinAnalysesController:
    def __init__(self):
        pass
    
    def solve_analyses(self, params):
        solver = FinSolver(params["fin_geometry"], params["solver_method"])
        data = self.__clean_data(params["data"])
        return solver.find_temp_distribuition(data)
        
    def __clean_data(self, data):
        new_data = data
        new_data["dimensions"]["radius"] = data["dimensions"]["radius"]/1000
        new_data["fin_length"] = data["fin_length"]/1000
        return new_data
    