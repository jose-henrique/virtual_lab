import pickle
import os
from model.utils.resource_path import resource_path

class PropertiesGetter:
    def __init__(self):
        self.properties = {}
        script_dir = os.path.dirname(__file__)
        with open(resource_path(os.path.join(script_dir, "../data/materials_properties.pkl")), 'rb') as f:
           self.properties = pickle.load(f)

    def list_materials(self, category=None):
        """List material keys, optionally only those of one category (e.g. "metal")."""
        return [
            name for name, properties in self.properties.items()
            if category is None or properties.get("category") == category
        ]

    def get_material(self, material):
        return self.properties[material]