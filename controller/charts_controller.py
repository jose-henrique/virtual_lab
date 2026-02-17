from view.chart_view import ChartView


class ChartsController:
    def __init__(self):
        pass
    
    def new_chart(self, params={}):
        chart_view = ChartView()
        chart_view.base_window()