import pathlib

from deephaven.plugin import Registration
from deephaven.plugin.js import JsType

from importlib.resources import files, as_file
from contextlib import contextmanager
from typing import Generator


@contextmanager
def _path() -> Generator[pathlib.Path, None, None]:
    with as_file(files(__package__)) as package:
        yield package / "data" / "package" / "package.json"


class PlotlyJs(JsType):
    @contextmanager
    def path(self) -> Generator[pathlib.Path, None, None]:
        # is this the same as return _path()?
        with _path() as path:
            yield path


class PlotlyJsRegistration(Registration):
    @classmethod
    def register_into(cls, callback: Registration.Callback) -> None:
        callback.register(PlotlyJs)
