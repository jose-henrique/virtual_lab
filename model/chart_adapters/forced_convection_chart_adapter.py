class ForcedConvectionChartAdapter:
    x_label = "Position along the tube (m)"

    def get_chart_data(self, data):
        profile = data.get("results", {}).get("profile", [])
        return [
            [point.get("position") for point in profile],
            [point.get("fluid_temperature") for point in profile],
        ]