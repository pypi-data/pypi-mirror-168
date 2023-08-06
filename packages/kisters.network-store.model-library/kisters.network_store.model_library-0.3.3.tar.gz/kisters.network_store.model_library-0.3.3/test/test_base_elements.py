import json
from typing import Any, Dict
from kisters.network_store.model_library.base import BaseElement

import pytest

elements = [
    {
        "domain": "test",
        "element_class": "BaseElement",
        "uid": "good_element_1",
        "display_name": "custom_name",
        "created": "1991-01-01T23:59:00",
        "deleted": "1991-01-02T23:59:00",
        "user_metadata": {
            "data_fl": 99.99,
            "data_int": 1000,
            "data_str": "árvíztűrő tükörfúrógép",
            "is_tested": True,
        },
        "time_series_mappings": [
            {
                "time_series": {
                    "store_id": "datasphere",
                    "path": "ts_path_id_max_flow",
                    "t0": "1991-01-01T23:59:00",
                    "dispatch_info": "1234abc",
                    "ensemble_member": "1",
                },
                "element": {"attribute": "max_flow"},
            },
            {
                "time_series": {
                    "store_id": "datasphere",
                    "path": "ts_path_id_min_flow",
                    # "t0": "1991-01-01T23:59",
                    "dispatch_info": "1234abc",
                    "ensemble_member": "1",
                },
                "element": {"attribute": "min_flow"},
            },
        ],
    },
    {
        "domain": "test",
        "element_class": "BaseElement",
        "uid": "uid_OK",
        "display_name": "something_else_than_uid_OK",
        "user_metadata": {
            "data_fl": 99.99,
            "data_int": 1000,
            "data_str": "árvíztűrő tükörfúrógép",
            "is_tested": True,
        },
    },
]

bad_elements = [
    {
        "domain": "test",
        "element_class": "BaseElement",
        "uid": "bad_element_1",
        "display_name": "",
        "created": "Long ago",  # ValueError
        "deleted": "Not that long ago",  # ValueError
        "user_metadata": {
            "data_fl": 99.99,
            "data_int": 1000,
            "data_str": "árvíztűrő tükörfúrógép",
            "is_tested": True,
            "invalid_field": {"Nested": "dict"},  # ValueError
        },
        "time_series_mappings": [
            {
                "time_series": {
                    "store_id": "datasphere",
                    "path": "ts_path_id_max_flow",
                    "t0": "1991-01-01T23:59",
                    "dispatch_info": "1234abc",
                    "ensemble_member": "1",
                },
                "element": {"attribute": "max_flow"},
            },
            {
                "time_series": {
                    "store_id": "datasphere",
                    "path": "ts_path_id_min_flow",
                    "t0": "1991-01-01T23:59",
                    "dispatch_info": "1234abc",
                    "ensemble_member": "1",
                },
                "element": {"attribute": "min_flow"},
            },
        ],
    },
    {
        "domain": "test",
        "element_class": "BaseElement",
        "uid": "bad_element_1./%",
        "display_name": "",
        "user_metadata": {
            "data_fl": 99.99,
            "data_int": 1000,
            "data_str": "árvíztűrő tükörfúrógép",
            "is_tested": True,
        },
    },
    {
        "domain": "test",
        "element_class": "BaseElement",
        "uid": "uid_OK",
        "display_name": "",
        "user_metadata": {
            "data_fl": 99.99,
            "data_int": 1000,
            "data_str": "árvíztűrő tükörfúrógép",
            "is_tested": True,
            "invalid_field": ["Lists", "are", "not", "cool"],
        },
    },
]


@pytest.mark.parametrize("element", elements)
def test_parse(element: Dict[str, Any]) -> None:
    instance = BaseElement.parse_obj(element)
    reserialised = json.loads(instance.json(exclude_none=True))
    assert element == reserialised


@pytest.mark.parametrize("element", bad_elements)
def test_parse_bad(element: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        BaseElement.parse_obj(element)
