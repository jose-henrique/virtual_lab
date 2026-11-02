from gettext import gettext as _


class ForcedConvectionSerializer:
    def serialize(self, payload):
        results = payload.get("results", {})
        rows = [
            [_("Analyze Data")],
            [_("Analyze Type"), _("Internal Forced Convection")],
            [_("Velocity (m/s)"), results.get("velocity")],
            [_("Inner Diameter (m)"), results.get("diameter")],
            [_("Tube Length (m)"), results.get("length")],
            [_("Inlet Temperature (°C)"), results.get("inlet_temperature")],
            [_("Wall Temperature (°C)"), results.get("wall_temperature")],
            [_("Density (kg/m³)"), results.get("density")],
            [_("Dynamic Viscosity (Pa.s)"), results.get("viscosity")],
            [_("Thermal Conductivity (W/m.K)"), results.get("thermal_conductivity")],
            [_("Specific Heat (J/kg.K)"), results.get("specific_heat")],
            [_("Correlation"), results.get("correlation")],
            [_("Reynolds Number"), results.get("reynolds_number")],
            [_("Prandtl Number"), results.get("prandtl_number")],
            [_("Nusselt Number"), results.get("nusselt_number")],
            [_("Convection Coefficient (W/m².K)"), results.get("heat_transfer_coefficient")],
            [_("Mass Flow Rate (kg/s)"), results.get("mass_flow_rate")],
            [_("Outlet Temperature (°C)"), results.get("outlet_temperature")],
            [_("Heat Rate (W)"), results.get("heat_rate")],
            [_("Heat Flux (W/m²)"), results.get("heat_flux")],
            [],
            [_("Position (m)"), _("Fluid Temperature (°C)"), _("Cumulative Heat Rate (W)")],
        ]
        for point in results.get("profile", []):
            rows.append([
                point.get("position"),
                point.get("fluid_temperature"),
                point.get("heat_rate"),
            ])
        return rows