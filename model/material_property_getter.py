import pickle
import os

class PropertiesGetter:
    def __init__(self):
        self.properties = {}
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir, "..\data\materials_properties.pkl"), 'rb') as f:
           self.properties = pickle.load(f)

    def list_materials(self):
        materials_list = []
        for i in self.properties:
            materials_list.append(i)
        return materials_list

    def get_material(self, material):
        return self.properties[material]