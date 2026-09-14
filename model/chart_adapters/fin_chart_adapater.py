class FinChartAdapter:
    def __init__(self):
        pass

    def get_chart_data(self, data):
        temps = data.get("results", {}).get("temperatures", [])
                    
        return [
            [item["relative_length"] for item in temps],
            [item["local_temp"] for item in temps],
        ]