import urllib.request
import tarfile
import io
import pathlib

__package_name__ = "deephaven_plugin_plotly_js"
__version__ = "0.1.0.dev4"  # needs to be static

__npm_org__ = "@deephaven"
__npm_package__ = "js-plugin-plotly"
__npm_version__ = "0.1.0"


def _npm_url():
    return f"https://registry.npmjs.org/{__npm_org__}/{__npm_package__}/-/{__npm_package__}-{__npm_version__}.tgz"


def _data_path(dst):
    return pathlib.Path(dst) / __package_name__ / "data"


def _info_path(dst):
    return pathlib.Path(dst) / __package_name__ / "__info__.py"


# https://pdm.fming.dev/latest/pyproject/build/#custom-file-generation
def build(src, dst):
    with urllib.request.urlopen(_npm_url()) as tgz:
        with tarfile.open(fileobj=io.BytesIO(tgz.read()), mode="r") as tar:
            tar.extractall(_data_path(dst))

    with open(_info_path(dst), "w") as version_file:
        version_file.writelines(
            [
                f"__version__ = '{__version__}'\n",
                f"__npm_org__ = '{__npm_org__}'\n",
                f"__npm_package__ = '{__npm_package__}'\n",
                f"__npm_version__ = '{__npm_version__}'",
            ]
        )
