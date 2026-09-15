from gettext import gettext as _

from model.material_property_getter import PropertiesGetter


class ConductionSolver:
    """Solve one-dimensional conduction through a multilayer wall.

    For a series wall, each layer resistance is R_i = L_i / (k_i A_i).
    For parallel branches, conductances are added: 1 / R_total = sum(1 / R_i).
    The heat rate is q = (T_hot - T_cold) / R_total and exchanged heat is
    Q = q * time.
    """

    def __init__(self):
        self.errors = []

    def solve_conduction(self, data):
        self.errors = []
        self._validate(data)
        if self.errors:
            return False

        layers = []
        for index, layer in enumerate(data["layers"], start=1):
            material = PropertiesGetter().get_material(layer["material"])
            thickness = layer["thickness"] / 1000
            area = layer["area"]
            conductivity = material["thermal_conductivity"]
            resistance = thickness / (conductivity * area)
            layers.append({
                "index": index,
                "material": layer["material"],
                "thickness": thickness,
                "area": area,
                "thermal_conductivity": conductivity,
                "resistance": resistance,
            })

        if data["configuration"] == "series":
            total_resistance = sum(layer["resistance"] for layer in layers)
            heat_rate = (data["hot_temperature"] - data["cold_temperature"]) / total_resistance
            total_area = layers[0]["area"]
            layer_heat_rates = [heat_rate for layer in layers]
            profile = self._series_profile(layers, data, heat_rate)
        else:
            conductance = sum(1 / layer["resistance"] for layer in layers)
            total_resistance = 1 / conductance
            heat_rate = (data["hot_temperature"] - data["cold_temperature"]) / total_resistance
            total_area = sum(layer["area"] for layer in layers)
            layer_heat_rates = [
                (data["hot_temperature"] - data["cold_temperature"]) / layer["resistance"]
                for layer in layers
            ]
            profile = [
                {"position": layer["index"], "temperature": data["hot_temperature"],
                 "heat_rate": layer_heat_rates[index]}
                for index, layer in enumerate(layers)
            ]

        return {
            "configuration": data["configuration"],
            "layers": layers,
            "layer_heat_rates": layer_heat_rates,
            "profile": profile,
            "total_resistance": total_resistance,
            "heat_rate": heat_rate,
            "heat_flux": heat_rate / total_area,
            "heat_exchanged": heat_rate * data["time"],
            "hot_temperature": data["hot_temperature"],
            "cold_temperature": data["cold_temperature"],
            "time": data["time"],
        }

    def solve(self, data):
        return self.solve_conduction(data)

    def _series_profile(self, layers, data, heat_rate):
        profile = [{"position": 0.0, "temperature": data["hot_temperature"], "heat_rate": heat_rate}]
        position = 0.0
        temperature = data["hot_temperature"]
        for layer in layers:
            position += layer["thickness"]
            temperature -= heat_rate * layer["resistance"]
            profile.append({"position": position, "temperature": temperature, "heat_rate": heat_rate})
        return profile

    def _validate(self, data):
        if not isinstance(data, dict):
            self.errors.append(_("Conduction data must be provided"))
            return
        for field in ("configuration", "hot_temperature", "cold_temperature", "time", "layers"):
            if field not in data:
                self.errors.append(_(f"{field} must be provided"))
        if self.errors:
            return
        if data["configuration"] not in ("series", "parallel"):
            self.errors.append(_("Configuration must be series or parallel"))
        if data["hot_temperature"] <= data["cold_temperature"]:
            self.errors.append(_("Hot temperature must be greater than cold temperature"))
        if data["time"] <= 0:
            self.errors.append(_("Time must be greater than zero"))
        if not data["layers"]:
            self.errors.append(_("At least one wall layer is required"))
            return

        materials = PropertiesGetter().list_materials()
        for index, layer in enumerate(data["layers"], start=1):
            if layer.get("material") not in materials:
                self.errors.append(_(f"Layer {index} material is not registered"))
            if layer.get("thickness", 0) <= 0:
                self.errors.append(_(f"Layer {index} thickness must be greater than zero"))
            if layer.get("area", 0) <= 0:
                self.errors.append(_(f"Layer {index} area must be greater than zero"))