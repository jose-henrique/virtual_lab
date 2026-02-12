import math
import pickle
from model.material_property_getter import PropertiesGetter
from model.data_validation import DataValidation

class FinSolver(DataValidation):
    def __init__(self, fin_geometry, solver_method):
        self.fin_geometry = fin_geometry
        self.solver_method = solver_method
        self.errors = []

    
    def find_temp_distribuition(self, data):
        self.errors = []
        self.__basic_validation(data)
        self.__validations(data)
        if len(self.errors) > 0:
            return False
        
        properties = self.__load_material_properties(data["fin_material"])
        return self.__generate_array(data, properties)
            
        
    def find_local_temperature(self, array, env_temperature, base_temperature):
        self.errors = []
        array_with_temp = []
        self.__validations_local_temperature(array, env_temperature, base_temperature)
        if len(self.errors) > 0:
            return False
        for element in array:
            local_temp = ((base_temperature - env_temperature)*element["temp_distribuition"]) + env_temperature
            element["local_temp"] = local_temp
            array_with_temp.append(element)
        
        return array_with_temp
    
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
        convection_coefficient = data["convection_coefficient"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        m = (convection_coefficient * perimeter)/(thermal_conductivity * area)
        return math.exp(-(m*analyses_point))

    def __temp_distribuiton_adiabatic_fin(self, data, analyses_point, properties):
        convection_coefficient = data["convection_coefficient"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        m = (convection_coefficient * perimeter)/(thermal_conductivity * area)
        return (math.cosh(m*(data["fin_length"] - analyses_point)))/(math.cosh(m*data["fin_length"]))

    def __temp_distribuiton_specified_temp(self, data, analyses_point, properties):
        convection_coefficient = data["convection_coefficient"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        m = (convection_coefficient * perimeter)/(thermal_conductivity * area)
        teta_l = data["temp_end_fin"] - data["temp_env"]
        teta_b = data["temp_base"] - data["temp_env"]
        return (((teta_l/teta_b)*math.sinh(m*analyses_point))+(math.sinh(m*(data["fin_length"]-analyses_point))))/(math.sinh(m*data["fin_length"]))

    def __temp_distribuiton_convection(self, data, analyses_point, properties):
        convection_coefficient = data["convection_coefficient"]
        perimeter = self.__perimeter_solve(data["dimensions"])
        thermal_conductivity = properties["thermal_conductivity"]
        area = self.__area_solve(data["dimensions"])
        length = data["fin_length"]
        m = (convection_coefficient * perimeter)/(thermal_conductivity * area)
        return ((math.cosh(m*(length-analyses_point)))+((convection_coefficient/(m*thermal_conductivity))*math.sinh(m*(length-analyses_point))))/((math.cosh(m*length))+((convection_coefficient/(m*thermal_conductivity))*math.sinh(m*length)))

    def __basic_validation(self, data):
        if "convection_coefficient" not in data:
            raise ValueError("The convection coefficient must be present") 
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
            return math.pi*math.pow(dimensions["radius"], 2)

    def __load_material_properties(self, material):
        properties = PropertiesGetter()
        return properties.get_material(material)
    
    def __validations(self, data):
        self._validate_dimensions(data)
        self.validates("Length",data.get("fin_length"), validation="presence")
        self.validates("Length",data.get("fin_length"), validation="greather_than",base_number=0)
        self.validates("Convection Coefficient",data.get("convection_coefficient"), validation="greather_than",base_number=0)
        self.validates("Nodes",data.get("node_count"), validation="greather_than",base_number=0)
        self.validates("Material",data.get("fin_material"), validation="includes",array=PropertiesGetter().list_materials())
        
    def _validate_dimensions(self, data):
        if self.fin_geometry == 1:
            self.validates("Dimension a",data["dimensions"].get("a"), validation="presence")
            self.validates("Dimension b",data["dimensions"].get("b"), validation="presence")
        
            self.validates("Dimension a",data["dimensions"].get("a"),base_number=0, validation="greather_than")
            self.validates("Dimension b",data["dimensions"].get("b"),base_number=0, validation="greather_than")
        elif self.fin_geometry == 2:
            self.validates("Radius",data["dimensions"].get("radius"), validation="presence")
            self.validates("Radius",data["dimensions"].get("radius"),base_number=0, validation="greather_than")

    def __validations_local_temperature(self, array, env_temperature, base_temperature):
        print(array)
        self.validates("Elements array", array, validation="presence", message="The data about the problem must be provided")
        self.validates("Enviroment Temperature", env_temperature, validation="presence")
        self.validates("Base Temperature", base_temperature, validation="presence")

"""
data_sample = {
    "convection_coefficient": 12.3
    "dimensions": { "a": 12.3, "b": 12.3 }
    fin_legth: 12.3
    node_count: 12,
    fin_material: "carbon_steel"
}

data_sample2 = {
    "convection_coefficient": 12.3 m
    "dimensions": { "radius": 12.3 m }
    fin_legth: 12.3 m
    node_count: 12,
    fin_material: "carbon_steel"
}
"""
