# -*- coding: utf-8 -*-
import json
import re

from requests.exceptions import ConnectionError, HTTPError

from .services import update_component


def post_save(model, os_path, contents_manager, **kwargs):
    """Send notebooks to PlatIAgro Projects API after save."""
    # only do this for notebooks
    if model["type"] != "notebook":
        return

    match = re.search(r"components/(.*?)/(Experiment|Deployment).ipynb", os_path)

    if match:
        component_id = match.group(1)
        notebook_type = match.group(2)

        with open(os_path) as f:
            notebook = json.load(f)

        try:
            if notebook_type == "Experiment":
                update_component(component_id, experiment_notebook=notebook)
            else:
                update_component(component_id, deployment_notebook=notebook)
        except (ConnectionError, HTTPError) as e:
            print(str(e))


def setup_hooks(web_app):
    web_app.settings["contents_manager"].post_save_hook = post_save
