from gettext import gettext as _


class ConductionSerializer:
    def serialize(self, payload):
        analyze_data = payload.get("analyze_data", {})
        results = payload.get("results", {})
        rows = [[_("Analyze Data")],
                [_("Analyze Type"), _("Wall Conduction Analysis")],
                [_("Configuration"), results.get("configuration")],
                [_("Hot Temperature (°C)"), results.get("hot_temperature")],
                [_("Cold Temperature (°C)"), results.get("cold_temperature")],
                [_("Time (s)"), results.get("time")],
                [_("Total Thermal Resistance (K/W)"), results.get("total_resistance")],
                [_("Heat Rate (W)"), results.get("heat_rate")],
                [_("Heat Flux (W/m²)"), results.get("heat_flux")],
                [_("Heat Exchanged (J)"), results.get("heat_exchanged")],
                [],
                [_("Layer"), _("Material"), _("Thickness (m)"), _("Area (m²)"),
                 _("Thermal Conductivity (W/m.K)"), _("Resistance (K/W)"), _("Heat Rate (W)")]]

        layers = results.get("layers", analyze_data.get("layers", []))
        heat_rates = results.get("layer_heat_rates", [])
        for index, layer in enumerate(layers):
            rows.append([
                layer.get("index", index + 1), layer.get("material"), layer.get("thickness"),
                layer.get("area"), layer.get("thermal_conductivity"), layer.get("resistance"),
                heat_rates[index] if index < len(heat_rates) else None,
            ])

        rows.extend([[], [_("Position (m)"), _("Temperature (°C)"), _("Heat Rate (W)")]])
        for point in results.get("profile", []):
            rows.append([point.get("position"), point.get("temperature"), point.get("heat_rate")])
        return rows