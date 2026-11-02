import json

import dearpygui.dearpygui as dpg
from gettext import gettext as _

from model.utils.font_manager import FontManager


class DatasetView:
    def __init__(self, width, height, parent):
        self.width = width
        self.height = height
        self.parent = parent
        self.text_font = FontManager().get("text_roboto_regular_medium")

    def display_analyze_data(self, dataset_a, dataset_b):
        for tag in ("dataset_info_a", "dataset_info_b"):
            if dpg.does_item_exist(tag):
                dpg.delete_item(tag)

        for dataset, tag in ((dataset_a, "dataset_info_a"), (dataset_b, "dataset_info_b")):
            if dataset:
                with dpg.group(tag=tag, parent=self.parent):
                    self.__display_dataset(dataset, self.width / 2)
                    dpg.bind_item_font(tag, self.text_font)

    def __display_dataset(self, dataset, width):
        analyze_data = dataset.get("analyze_data") or {}
        results = dataset.get("results") or {}

        if not isinstance(analyze_data, dict):
            analyze_data = {"value": analyze_data}
        if not isinstance(results, dict):
            results = {"value": results}

        dpg.add_text(self.__label(dataset.get("type", "Analysis")), color=(255, 209, 102))
        if analyze_data:
            dpg.add_text(_("Input Data"), color=(190, 91, 16))
            self.__display_mapping(analyze_data, width)
        if results:
            dpg.add_text(_("Results"), color=(190, 91, 16))
            self.__display_mapping(results, width)

    def __display_mapping(self, values, width):
        scalar_values = [
            (key, value)
            for key, value in values.items()
            if not isinstance(value, (dict, list, tuple))
        ]
        nested_values = [
            (key, value)
            for key, value in values.items()
            if isinstance(value, (dict, list, tuple))
        ]

        if scalar_values:
            columns = min(3, len(scalar_values))
            with dpg.table(header_row=False, resizable=False, width=width):
                for _ in range(columns):
                    dpg.add_table_column()
                for start in range(0, len(scalar_values), columns):
                    with dpg.table_row():
                        for key, value in scalar_values[start:start + columns]:
                            with dpg.group():
                                dpg.add_text(self.__label(key), wrap=0, color=(190, 91, 16))
                                dpg.add_text(self.__format_value(value), color=(124, 246, 236))

        for key, value in nested_values:
            dpg.add_text(self.__label(key), color=(255, 209, 102))
            if isinstance(value, dict):
                self.__display_mapping(value, width)
            else:
                self.__display_sequence(value, width)

    def __display_sequence(self, values, width):
        if not values:
            return

        rows = [value for value in values if isinstance(value, dict)]
        if rows:
            columns = self.__table_columns(rows)
            if not columns:
                return
            with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                           borders_innerV=True, borders_outerV=True, scrollY=True,
                           width=width, height=max(120, self.height / 4)):
                for key in columns:
                    dpg.add_table_column(label=self.__label(key))
                for row in rows:
                    with dpg.table_row():
                        for key in columns:
                            dpg.add_text(self.__format_value(row.get(key)))
            return

        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True, scrollY=True,
                       width=width, height=max(120, self.height / 4)):
            dpg.add_table_column(label=_("#"))
            dpg.add_table_column(label=_("Value"))
            for index, value in enumerate(values, start=1):
                with dpg.table_row():
                    dpg.add_text(str(index))
                    dpg.add_text(self.__format_value(value))

    def __table_columns(self, rows):
        return list(dict.fromkeys(key for row in rows for key in row))

    def __label(self, value):
        return _(str(value).replace("_", " ").title())

    def __format_value(self, value):
        if isinstance(value, (dict, list, tuple)):
            return json.dumps(value, ensure_ascii=False)
        if isinstance(value, float):
            return f"{value:.6g}"
        return str(value) if value is not None else "-"

    def remove_infos(self):
        for tag in ("dataset_info_a", "dataset_info_b"):
            if dpg.does_item_exist(tag):
                dpg.delete_item(tag)