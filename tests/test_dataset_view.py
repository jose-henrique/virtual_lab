from view.data_results.dataset_view import DatasetView


def test_dataset_view_infers_columns_from_each_result_shape():
    view = DatasetView.__new__(DatasetView)
    fin_rows = [{"point": 0.1, "local_temp": 75.0}]
    wall_rows = [{"position": 0.0, "temperature": 100.0, "heat_rate": 20.0}]

    assert view._DatasetView__table_columns(fin_rows) == ["point", "local_temp"]
    assert view._DatasetView__table_columns(wall_rows) == ["position", "temperature", "heat_rate"]


def test_dataset_view_combines_columns_for_heterogeneous_rows():
    view = DatasetView.__new__(DatasetView)

    assert view._DatasetView__table_columns([{"first": 1}, {"second": 2}]) == ["first", "second"]