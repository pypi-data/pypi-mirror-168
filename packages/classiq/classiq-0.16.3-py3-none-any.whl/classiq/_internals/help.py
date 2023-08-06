import webbrowser
from typing import Optional

import classiq

DOCS_BASE_URL = "https://docs.classiq.io/"  # noqa: link


def open_help(version: Optional[str] = None) -> None:
    if version is None:
        version = classiq.__version__
    if version == "0.0.0":
        # Dev Environment
        url_suffix = "latest/"
    else:
        url_suffix = "-".join(version.split(".")[:-1]) + "/"
    webbrowser.open(DOCS_BASE_URL + url_suffix)
