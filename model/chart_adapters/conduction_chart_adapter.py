class ConductionChartAdapter:
    def get_chart_data(self, data):
        profile = data.get("results", {}).get("profile", [])
        return [
            [point.get("position") for point in profile],
            [point.get("temperature") for point in profile],
        ]