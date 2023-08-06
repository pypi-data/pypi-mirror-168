import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component("stramlit_firebase_remote_config_component", url="http://localhost:3001",)
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("stramlit_firebase_remote_config_component", path=build_dir)

def clean_params(params):
    return {k: v['_value'] for k, v in params.items() if '_value' in v}

def fbrc(config, clean=True, key=None):
    """Create a new instance of "fbrc".

    Parameters
    ----------
    config: config
        Firebase config
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    {}: A dictionary of remote parameters

    """
    component_value = _component_func(config=config, key=key, default={})

    if clean:
        return clean_params(component_value)
    else:
        return component_value


