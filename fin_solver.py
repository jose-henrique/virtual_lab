import math
import pickle
"""
data_sample = {
    "convection_coeficienty": 12.3
    "dimensions": { "a": 12.3, "b": 12.3 }
    fin_legth: 12.3
    node_count: 12,
    fin_material: "carbon_steel"
}

data_sample2 = {
    "convection_coeficienty": 12.3 m
    "dimensions": { "radius": 12.3 m }
    fin_legth: 12.3 m
    node_count: 12,
    fin_material: "carbon_steel"
}
"""
class FinSolver:
    def __init__(self, fin_geometry, solver_method):
        self.fin_geometry = fin_geometry
        self.solver_method = solver_method

    
    def find_temp_distribuition(self, data):
        self.__basic_validation(data)
        properties = self.__load_material_properties(data["fin_material"])
        print(self.__generate_array(data, properties))
    
    def __generate_array(self, data, properties):
        length = data["fin_length"]
        node_length = length/data["node_count"]
        point = length/data["node_count"]
        temp_array = []
        for i in range(0, data["node_count"]):
            if self.solver_method == 1:
                temp_array.append({"point": point, "temp_distribuition": self.__temp_distribuiton_infinity_fin(data, point, properties)})
            elif self.solver_method == 2:
                temp_array.append({"point": point, "temp_distribuition": self.__temp_distribuiton_adiabatic_fin(data, point, properties)})
            elif self.solver_method == 3:
                temp_array.append({"point": point, "temp_distribuition": self.__temp_distribuiton_specified_temp(data, point, properties)})
            elif self.solver_method == 4:
                temp_array.append({"point": point, "temp_distribuition": self.__temp_distribuiton_convection(data, point, properties)})
            
            point += node_length
        return temp_array


    def __temp_distribuiton_infinity_fin(self, data, analyses_point, properties):
        convection_coeficienty = data["convection_coeficienty"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        m = (convection_coeficienty * perimeter)/(thermal_conductivity * area)
        return math.exp(-(m*analyses_point))

    def __temp_distribuiton_adiabatic_fin(self, data, analyses_point, properties):
        convection_coeficienty = data["convection_coeficienty"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        m = (convection_coeficienty * perimeter)/(thermal_conductivity * area)
        return (math.cosh(m*(data["fin_length"] - analyses_point)))/(math.cosh(m*data["fin_length"]))

    def __temp_distribuiton_specified_temp(self, data, analyses_point, properties):
        convection_coeficienty = data["convection_coeficienty"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        m = (convection_coeficienty * perimeter)/(thermal_conductivity * area)
        teta_l = data["temp_end_fin"] - data["temp_env"]
        teta_b = data["temp_base"] - data["temp_env"]
        return (((teta_l/teta_b)*math.sinh(m*analyses_point))+(math.sinh(m*(data["fin_length"]-analyses_point))))/(math.sinh(m*data["fin_length"]))

    def __temp_distribuiton_convection(self, data, analyses_point, properties):
        convection_coeficienty = data["convection_coeficienty"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        length = data["fin_length"]
        m = (convection_coeficienty * perimeter)/(thermal_conductivity * area)
        return ((math.cosh(m*(length-analyses_point)))+((convection_coeficienty/(m*thermal_conductivity))*math.sinh(m*(length-analyses_point))))/((math.cosh(m*length))+((convection_coeficienty/(m*thermal_conductivity))*math.sinh(m*length)))

    def __basic_validation(self, data):
        if "convection_coeficienty" not in data:
            raise ValueError("The convection coeficienty must be present") 
        if "dimensions" not in data:
            raise ValueError("The dimensions must be present") 
        if "node_count" not in data:
            raise ValueError("The node count must be present") 
        if "fin_material" not in data:
            raise ValueError("The material must be present")
        if "fin_length" not in data:
            raise ValueError("The length must be present") 

    
    def __perimeter_solve(self, dimensions):
        # 1 for square 2 for circle
        if self.fin_geometry == 1:
            return (dimensions["a"]*2)+(dimensions["b"]*2)
        elif self.fin_geometry == 2:
            return 2*math.pi*dimensions["radius"]

    def __area_solve(self, dimensions):
        # 1 for square 2 for circle
        if self.fin_geometry == 1:
            return dimensions["a"]*dimensions["b"]
        elif self.fin_geometry == 2:
            return pi*math.pow(dimensions["radius"], 2)

    def __load_material_properties(self, material):
        properties = {}
        with open('materials_properties.pkl', 'rb') as f:
            properties = pickle.load(f)

        return properties[material]



solver = FinSolver(1, 1)
solver.find_temp_distribuition({
    "convection_coeficienty": 12.3,
    "dimensions": { "a": 12.3, "b": 12.3 },
    "fin_length": 0.1,
    "node_count": 3,
    "fin_material": "carbon_steel"
})
print("=-"*20)
solver_2 = FinSolver(1, 2)
solver_2.find_temp_distribuition({
    "convection_coeficienty": 12.3,
    "dimensions": { "a": 12.3, "b": 12.3 },
    "fin_length": 0.1,
    "node_count": 3,
    "fin_material": "carbon_steel"
})
print("=-"*20)
solver_3 = FinSolver(1, 3)
solver_3.find_temp_distribuition({
    "convection_coeficienty": 12.3,
    "dimensions": { "a": 12.3, "b": 12.3 },
    "fin_length": 0.1,
    "node_count": 3,
    "fin_material": "carbon_steel",
    "temp_end_fin": 60,
    "temp_base": 90,
    "temp_env": 25
})

print("=-"*20)
solver_4 = FinSolver(1, 4)
solver_4.find_temp_distribuition({
    "convection_coeficienty": 12.3,
    "dimensions": { "a": 12.3, "b": 12.3 },
    "fin_length": 0.1,
    "node_count": 3,
    "fin_material": "carbon_steel",
    "temp_end_fin": 60,
    "temp_base": 90,
    "temp_env": 25
})


