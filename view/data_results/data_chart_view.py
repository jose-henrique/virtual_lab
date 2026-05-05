import dearpygui.dearpygui as dpg
from gettext import gettext as _


class DataChartView:
    def __init__(self, height):
        self.window_name = "data_chart_view"
        self.width_window = 300
        self.height_window = height

    def base_window(self):
        if dpg.does_item_exist(self.window_name):
            dpg.configure_item(self.window_name, show=True)
        else:
            with dpg.child_window(label=_("DATA CHART"), tag=self.window_name,
            always_use_window_padding=True,
            height= self.height_window,
            show=True):
                with dpg.plot(label="Meu Gráfico", width=-1, height=-1):
                    # Eixos
                    dpg.add_plot_axis(dpg.mvXAxis, label="Eixo X")
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Eixo Y")

                    # Dados
                    x = [0, 1, 2, 3, 4]
                    y = [0, 1, 4, 9, 16]
                    y2 = [0, 1, 8, 27, 64]

                    # Série de linha
                    dpg.add_line_series(x, y, label="y = x²", parent=y_axis)
                    dpg.add_line_series(x, y2, label="y = x³", parent=y_axis)

