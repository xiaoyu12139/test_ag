import inspect
import base

def pytest_collection_modifyitems(items):
    skip_func_names = [
        name for name, func in inspect.getmembers(base, inspect.isfunction)
    ]

    for item in list(items):
        if item.name in skip_func_names:
            items.remove(item)