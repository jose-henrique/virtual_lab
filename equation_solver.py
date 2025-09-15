import yaml

class EquationSolver:
    def __init__(self, temp_1, temp_2, thickness, area, conductivity):
        self.delta_temp = temp_1 - temp_2
        self.thickness = thickness
        self.area = area
        self.conductivity = conductivity

    

    def solve_conduction_heat(self):
        self.open_yaml_file()
        return (self.conductivity * self.area)*(self.delta_temp/self.thickness)

    def open_yaml_file(self):
        with open("./material_properties.yml") as stream:
            try:
                print(yaml.safe_load(stream)["cobre"]["condutividade_termica"])
            except yaml.YAMLError as exc:
                print(exc)


solver = EquationSolver(45, 30, 0.12, 1, 300)
print(solver.solve_conduction_heat()/1000)