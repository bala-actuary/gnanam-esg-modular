"""
Demo aggregation plugin for RADF.
This function will be auto-registered if the plugin loader is called.
"""


def aggregate_demo(model_outputs, config):
    """Demo aggregation method: returns the number of models and a static value."""
    return {"demo": True, "num_models": len(model_outputs), "static_value": 42}
