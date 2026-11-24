import os
import pickle

# Propriedades aproximadas a ~300 K (Çengel, Tabelas A-3, A-5 e A-6).
# "category" separa metais (usados nas aletas) de isolantes/materiais de construção
# (disponíveis para a parede composta).

materials = {
    "carbon_steel": {
        "density": 7850,
        "thermal_conductivity": 54,
        "specific_heat": 490,
        "category": "metal",
        "thermal_expansion": 0.000012
    },
    "aluminum": {
        "density": 2700,
        "thermal_conductivity": 237,
        "specific_heat": 900,
        "category": "metal",
        "thermal_expansion": 0.000023
    },
    "copper": {
        "density": 8960,
        "thermal_conductivity": 401,
        "specific_heat": 385,
        "category": "metal",
        "thermal_expansion": 0.0000165
    },
    "brass": {
        "density": 8530,
        "thermal_conductivity": 109,
        "specific_heat": 380,
        "category": "metal",
        "thermal_expansion": 0.000019
    },
    "cast_iron": {
        "density": 7200,
        "thermal_conductivity": 55,
        "specific_heat": 460,
        "category": "metal",
        "thermal_expansion": 0.000011
    },
    "common_brick": {
        "density": 1922,
        "thermal_conductivity": 0.72,
        "specific_heat": 835,
        "category": "building",
    },
    "concrete": {
        "density": 2300,
        "thermal_conductivity": 1.4,
        "specific_heat": 880,
        "category": "building",
    },
    "wood_pine": {
        "density": 510,
        "thermal_conductivity": 0.12,
        "specific_heat": 1380,
        "category": "building",
    },
    "glass_wool": {
        "density": 24,
        "thermal_conductivity": 0.038,
        "specific_heat": 835,
        "category": "insulation",
    },
    "eps": {
        "density": 20,
        "thermal_conductivity": 0.033,
        "specific_heat": 1210,
        "category": "insulation",
    },
}

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materials_properties.pkl")
with open(output_path, 'wb') as f:
    pickle.dump(materials, f)