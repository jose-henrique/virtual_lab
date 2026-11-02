from gettext import gettext as _
import math


class ForcedConvectionSolver:
    """Model internal forced convection in a circular tube."""

    def __init__(self):
        self.errors = []

    def solve(self, data):
        self.errors = []
        self._validate(data)
        if self.errors:
            return False

        diameter = data["diameter"]
        length = data["length"]
        velocity = data["velocity"]
        density = data["density"]
        viscosity = data["viscosity"]
        conductivity = data["thermal_conductivity"]
        specific_heat = data["specific_heat"]
        reynolds = density * velocity * diameter / viscosity
        prandtl = viscosity * specific_heat / conductivity
        nusselt, correlation = self._nusselt_number(reynolds, prandtl)
        heat_transfer_coefficient = nusselt * conductivity / diameter
        flow_area = math.pi * diameter ** 2 / 4
        heat_transfer_area = math.pi * diameter * length
        mass_flow_rate = density * velocity * flow_area
        capacity_rate = mass_flow_rate * specific_heat
        inlet_temperature = data["inlet_temperature"]
        wall_temperature = data["wall_temperature"]
        exponent = heat_transfer_coefficient * heat_transfer_area / capacity_rate
        outlet_temperature = wall_temperature - (
            wall_temperature - inlet_temperature
        ) * math.exp(-exponent)
        heat_rate = capacity_rate * (outlet_temperature - inlet_temperature)

        profile = []
        for index in range(21):
            position = length * index / 20
            fluid_temperature = wall_temperature - (
                wall_temperature - inlet_temperature
            ) * math.exp(-heat_transfer_coefficient * math.pi * diameter * position / capacity_rate)
            profile.append({
                "position": position,
                "fluid_temperature": fluid_temperature,
                "heat_rate": capacity_rate * (fluid_temperature - inlet_temperature),
            })

        return {
            "reynolds_number": reynolds,
            "prandtl_number": prandtl,
            "nusselt_number": nusselt,
            "correlation": correlation,
            "heat_transfer_coefficient": heat_transfer_coefficient,
            "flow_area": flow_area,
            "heat_transfer_area": heat_transfer_area,
            "mass_flow_rate": mass_flow_rate,
            "outlet_temperature": outlet_temperature,
            "heat_rate": heat_rate,
            "heat_flux": heat_rate / heat_transfer_area,
            "inlet_temperature": inlet_temperature,
            "wall_temperature": wall_temperature,
            "velocity": velocity,
            "diameter": diameter,
            "length": length,
            "density": density,
            "viscosity": viscosity,
            "thermal_conductivity": conductivity,
            "specific_heat": specific_heat,
            "profile": profile,
        }

    def solve_forced_convection(self, data):
        return self.solve(data)

    def _nusselt_number(self, reynolds, prandtl):
        if reynolds < 2300:
            return 3.66, "Laminar, fully developed"

        turbulent_nusselt = self._gnielinski_nusselt(max(reynolds, 3000), prandtl)
        if reynolds < 3000:
            fraction = (reynolds - 2300) / 700
            return 3.66 + fraction * (turbulent_nusselt - 3.66), "Transition estimate"
        return turbulent_nusselt, "Gnielinski"

    def _gnielinski_nusselt(self, reynolds, prandtl):
        friction_factor = (0.79 * math.log(reynolds) - 1.64) ** -2
        return (
            (friction_factor / 8) * (reynolds - 1000) * prandtl
            / (1 + 12.7 * math.sqrt(friction_factor / 8) * (prandtl ** (2 / 3) - 1))
        )

    def _validate(self, data):
        if not isinstance(data, dict):
            self.errors.append(_("Forced convection data must be provided"))
            return

        required_fields = (
            "diameter", "length", "velocity", "density", "viscosity",
            "thermal_conductivity", "specific_heat", "inlet_temperature",
            "wall_temperature",
        )
        for field in required_fields:
            value = data.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
                self.errors.append(_(f"{field} must be a finite number"))
        if self.errors:
            return

        for field in ("diameter", "length", "velocity", "density", "viscosity", "thermal_conductivity", "specific_heat"):
            if data[field] <= 0:
                self.errors.append(_(f"{field} must be greater than zero"))
        if self.errors:
            return

        prandtl = data["viscosity"] * data["specific_heat"] / data["thermal_conductivity"]
        reynolds = data["density"] * data["velocity"] * data["diameter"] / data["viscosity"]
        if reynolds > 5e6:
            self.errors.append(_("Reynolds number exceeds the supported correlation range"))
        if reynolds >= 2300 and not 0.5 <= prandtl <= 2000:
            self.errors.append(_("Turbulent correlation requires Prandtl number between 0.5 and 2000"))