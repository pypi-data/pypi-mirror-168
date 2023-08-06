import urllib.request
import tarfile
import io
import pathlib

__version__ = '0.1.0.dev0' # needs to be static
__npm_version__ = '0.1.0'
__package_name__ = 'deephaven_plugin_plotly_js'


def _url():
    return f"https://registry.npmjs.org/@deephaven/js-plugin-plotly/-/js-plugin-plotly-{__npm_version__}.tgz"


def _data_path(dst):
    return pathlib.Path(dst) / __package_name__ / 'data'


def _version_path(dst):
    return pathlib.Path(dst) / __package_name__ / '__version__.py'


# https://pdm.fming.dev/latest/pyproject/build/#custom-file-generation
def build(src, dst):
    with urllib.request.urlopen(_url()) as tgz:
        with tarfile.open(fileobj=io.BytesIO(tgz.read()), mode='r') as tar:
            tar.extractall(_data_path(dst))

    with open(_version_path(dst), 'w') as version_file:
        version_file.write(f"__version__ = '{__version__}'")
