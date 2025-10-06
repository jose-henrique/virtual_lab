import pickle

materials = {
    "carbon_steel": {
        "density": 7850,
        "thermal_conductivity": 54,
        "specific_heat": 490,
        "thermal_expansion": 0.000012
    },
    "aluminum": {
        "density": 2700,
        "thermal_conductivity": 237,
        "specific_heat": 900,
        "thermal_expansion": 0.000023
    },
    "copper": {
        "density": 8960,
        "thermal_conductivity": 401,
        "specific_heat": 385,
        "thermal_expansion": 0.0000165
    },
    "brass": {
        "density": 8530,
        "thermal_conductivity": 109,
        "specific_heat": 380,
        "thermal_expansion": 0.000019
    },
    "cast_iron": {
        "density": 7200,
        "thermal_conductivity": 55,
        "specific_heat": 460,
        "thermal_expansion": 0.000011
    }
}

with open('materials_properties.pkl', 'wb') as f:
    pickle.dump(materials, f)