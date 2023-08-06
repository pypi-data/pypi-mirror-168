import json

import deephaven_plugin_plotly_js
from deephaven_plugin_plotly_js.__info__ import (
    __npm_org__,
    __npm_package__,
    __npm_version__,
)


def _read_package_json():
    with deephaven_plugin_plotly_js.PlotlyJs().path() as path:
        with open(path) as package_json:
            return json.load(package_json)


def test_correct_package_info():
    package_json = _read_package_json()
    assert package_json["name"] == f"{__npm_org__}/{__npm_package__}"
    assert package_json["version"] == __npm_version__
