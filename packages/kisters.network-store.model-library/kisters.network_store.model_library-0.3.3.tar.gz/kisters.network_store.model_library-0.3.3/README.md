# kisters.network_store.model_library

Base models and associated utilities for the KISTERS Network Store.

## A Note on Entrypoints

To publish a model library using entrypoints, add the domain and path to the
root directory of your library to the entrypoint
`kisters.network_store.model_library.util`. For example, the model library for
the water domain looks as follows:

```python
entry_points = {
    "kisters.network_store.model_library.util": [
        "water = kisters.network_store.model_library.water"
    ],
}
```

For the entrypoint to correctly identify the models in the library, the root
`__init__.py` must include the `links` and `nodes` modules. Furthermore, the
parent node of your library's nodes is expected to be called `_Node` and the
parent link is expected to be called `_Link`. All links and nodes in your
library will inherit from these two elements.
