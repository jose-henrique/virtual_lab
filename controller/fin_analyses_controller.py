from model.fin_solver import FinSolver


class FinAnalysesController:
    def __init__(self):
        pass
    
    def solve_analyses(self, params):
        #solver = FinSolver(params["fin_geometry"], params["solver_method"])
        #data = self.__clean_data(params["data"])
        #temp_array = solver.find_local_temperature(solver.find_temp_distribuition(data), params["env_temperature"], params["base_temperature"])
        #return {'temperatures': temp_array, 'base_temperature': params["base_temperature"]}
        solver = FinSolver(2, 1)
        data = {'convection_coefficient': 15.0, 'dimensions': {'radius': 0.003}, 'fin_length': 0.008, 'node_count': 10, 'fin_material': 'copper'}
        temp_distribuition = solver.find_temp_distribuition(data)
        if temp_distribuition:
            print("sucesso")
            temp_array = solver.find_local_temperature(temp_distribuition, 25, 80)
            return {'temperatures': temp_array, 'base_temperature': 80, 'status': 0}
        else:
            return {'errors': solver.errors, 'status': -1}
        
        
    def __clean_data(self, data):
        new_data = data
        new_data["dimensions"]["radius"] = data["dimensions"]["radius"]/1000
        new_data["fin_length"] = data["fin_length"]/1000
        return new_data
    