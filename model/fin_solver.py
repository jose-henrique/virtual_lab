import math
import pickle
from model.material_property_getter import PropertiesGetter
from model.data_validation import DataValidation
from gettext import gettext as _

class FinSolver(DataValidation):
    def __init__(self, fin_geometry, solver_method):
        self.fin_geometry = fin_geometry
        self.solver_method = solver_method
        self.errors = []

    
    def solve_fin(self, data):
        self.errors = []
        self.__basic_validation(data)
        self.__validations(data)
        if len(self.errors) > 0:
            return False
        
        properties = self.__load_material_properties(data["fin_material"])
        self.__perimeter_solve(data["dimensions"])
        self.__area_solve(data["dimensions"])
        heat_transfer = self.__calculate_heat_transfer(data, properties)
        return {
            "area": self.area,
            "perimeter": self.perimeter,
            "fin_efficience": self.__solve_fin_efficience(heat_transfer, data["convection_coefficient"], (data.get("base_temperature") - data.get("env_temperature"))),
            "temp_results": self.__generate_array(data, properties),
            "heat_transfer": heat_transfer
            }
            
        
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
    
    def __calculate_heat_transfer(self, data, properties):
        if self.solver_method == 1:
            heat_transfer = self.__heat_transfer_infinity_fin(data, properties)
        elif self.solver_method == 2:
            heat_transfer = self.__heat_transfer_adiabatic_fin(data, properties)
        elif self.solver_method == 3:
            heat_transfer = self.__heat_transfer_specified_temp(data, properties)
        elif self.solver_method == 4:
            heat_transfer = self.__heat_transfer_convection(data, properties)
        
        return heat_transfer
    
    
    def __generate_array(self, data, properties):
        length = data["fin_length"]
        node_length = length/data["node_count"]
        point = length/data["node_count"]
        temp_array = []
        for i in range(0, data["node_count"]):
            if self.solver_method == 1:
                temp_distribuition =  self.__temp_distribuiton_infinity_fin(data, point, properties)
            elif self.solver_method == 2:
                temp_distribuition = self.__temp_distribuiton_adiabatic_fin(data, point, properties)
            elif self.solver_method == 3:
                temp_distribuition = self.__temp_distribuiton_specified_temp(data, point, properties)
            elif self.solver_method == 4:
                temp_distribuition = self.__temp_distribuiton_convection(data, point, properties)
            
            temp_array.append(
                {
                    "point": point, 
                    "temp_distribuition": temp_distribuition,
                    "relative_length": point / length
                })
            
            point += node_length
        return temp_array


    def __temp_distribuiton_infinity_fin(self, data, analyses_point, properties):
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        m = (convection_coefficient * self.perimeter)/(thermal_conductivity * self.area)
        return math.exp(-(m*analyses_point))

    def __heat_transfer_infinity_fin(self,data, properties):
        base_temperature = data["base_temperature"]
        env_temperature = data["env_temperature"]
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        greater_m = math.sqrt(convection_coefficient * self.perimeter * thermal_conductivity * self.area) * (base_temperature - env_temperature)
        return greater_m

    def __temp_distribuiton_adiabatic_fin(self, data, analyses_point, properties):
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        m = (convection_coefficient * self.perimeter)/(thermal_conductivity * self.area)
        return (math.cosh(m*(data["fin_length"] - analyses_point)))/(math.cosh(m*data["fin_length"]))

    def __heat_transfer_adiabatic_fin(self, data, properties):
        base_temperature = data["base_temperature"]
        env_temperature = data["env_temperature"]
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        m = (convection_coefficient * self.perimeter)/(thermal_conductivity * self.area)
        greater_m = math.sqrt(convection_coefficient * self.perimeter * thermal_conductivity * self.area) * (base_temperature - env_temperature)
        return greater_m * math.tanh(m*data["fin_length"])

    def __temp_distribuiton_specified_temp(self, data, analyses_point, properties):
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        m = (convection_coefficient * self.perimeter)/(thermal_conductivity * self.area)
        teta_l = data.get("temp_end_fin") - data.get("env_temperature")
        teta_b = data.get("base_temperature") - data.get("env_temperature")
        return (((teta_l/teta_b)*math.sinh(m*analyses_point))+(math.sinh(m*(data["fin_length"]-analyses_point))))/(math.sinh(m*data["fin_length"]))

    def __heat_transfer_specified_temp(self, data, properties):
        base_temperature = data["base_temperature"]
        env_temperature = data["env_temperature"]
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        theta_l = data["temp_end_fin"] - env_temperature
        theta_b = base_temperature - env_temperature
        m = (convection_coefficient * self.perimeter)/(thermal_conductivity * self.area)
        greater_m = math.sqrt(convection_coefficient * self.perimeter * thermal_conductivity * self.area) * (base_temperature - env_temperature)
        return greater_m * ((math.cosh(m*data["fin_length"]) - (theta_l/theta_b))/ math.sinh(m*data["fin_length"]))

    def __temp_distribuiton_convection(self, data, analyses_point, properties):
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        length = data["fin_length"]
        m = (convection_coefficient * self.perimeter)/(thermal_conductivity * self.area)
        return ((math.cosh(m*(length-analyses_point)))+((convection_coefficient/(m*thermal_conductivity))*math.sinh(m*(length-analyses_point))))/((math.cosh(m*length))+((convection_coefficient/(m*thermal_conductivity))*math.sinh(m*length)))

    def __heat_transfer_convection(self, data, properties):
        base_temperature = data["base_temperature"]
        env_temperature = data["env_temperature"]
        convection_coefficient = data["convection_coefficient"]
        thermal_conductivity = properties["thermal_conductivity"]
        length = data["fin_length"]
        m = (convection_coefficient * self.perimeter)/(thermal_conductivity * self.area)
        greater_m = math.sqrt(convection_coefficient * self.perimeter * thermal_conductivity * self.area) * (base_temperature - env_temperature)
        return greater_m * ((math.sinh(m*length) + ((convection_coefficient/(m*thermal_conductivity))*math.cosh(m*length)))/(math.cosh(m*length) + ((convection_coefficient/(m*thermal_conductivity)) * math.sinh(m*length))))
    
    
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
            self.perimeter = (dimensions["a"]*2)+(dimensions["b"]*2)
        elif self.fin_geometry == 2:
            self.perimeter = 2*math.pi*dimensions["radius"]

    def __area_solve(self, dimensions):
        # 1 for square 2 for circle
        if self.fin_geometry == 1:
            self.area = dimensions["a"]*dimensions["b"]
        elif self.fin_geometry == 2:
            self.area = math.pi*math.pow(dimensions["radius"], 2)

    def __load_material_properties(self, material):
        properties = PropertiesGetter()
        return properties.get_material(material)
    
    def __solve_fin_efficience(self, heat_transfer, convection_coefficient, theta_b):
        return heat_transfer / (convection_coefficient * self.area * theta_b)
    
    def __validations(self, data):
        self.validates("Solver",self.solver_method, validation="presence", message=_("Solver Method Must Be Selected"))
        self.validates("Geometry",self.fin_geometry, validation="presence")
        self.validates("Length",data.get("fin_length"), validation="presence")
        self._validate_dimensions(data)
        self.validates("Length",data.get("fin_length"), validation="greather_than",base_number=0)
        self.validates("Convection Coefficient",data.get("convection_coefficient"), validation="greather_than",base_number=0)
        self.validates("Nodes",data.get("node_count"), validation="greather_than",base_number=9)
        self.validates("Material",data.get("fin_material"), validation="includes",array=PropertiesGetter().list_materials())
        self.validates("Enviroment Temperature", data.get("env_temperature"), validation="presence")
        if self.solver_method == 3:
            self.validates("Specified Temperature",data.get("temp_end_fin"), validation="presence")
        
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
        self.validates("Elements array", array, validation="presence", message=_("The data about the problem must be provided"))
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
