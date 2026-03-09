import json
import keyword
import re
import typing as t
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_SPEC_URL: str = "https://tonapi.io/v2/openapi.yml"
CONFIG_PATH: Path = Path(__file__).resolve().parent / "config.yml"
TEMPLATES_DIR: Path = Path(__file__).resolve().parent / "templates"

env: Environment = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)

TYPE_MAP: t.Dict[str, str] = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
}

NON_MODEL_TYPES: t.Set[str] = {
    "str", "int", "float", "bool", "bytes", "t.Dict[str, t.Any]",
}

_spec_cache: t.Optional[dict] = None


def _fetch_url(url: str, timeout: float = 15.0) -> bytes:
    """Fetch raw bytes from a URL.

    :param url: HTTP/HTTPS URL.
    :param timeout: network timeout in seconds.
    :return: response body bytes.
    :raises RuntimeError: on network or HTTP errors.
    """
    try:
        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "User-Agent": "pytonapi-codegen (+https://github.com/nessshon/pytonapi)",
                "Accept": "application/x-yaml,text/yaml,text/plain,*/*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except HTTPError as e:
        raise RuntimeError(f"Failed to fetch spec: {e} ({url})") from e
    except URLError as e:
        raise RuntimeError(f"Failed to fetch spec: {e.reason} ({url})") from e


def load_spec(source: t.Optional[str] = None) -> dict:
    """Load the OpenAPI specification from a URL or local file.

    The result is cached after the first call so that multiple
    generation stages reuse the same spec without extra fetches.

    :param source: URL or file path, or ``None``.
    :return: parsed OpenAPI spec dictionary.
    :raises RuntimeError: on fetch/parse failure.
    """
    global _spec_cache
    if _spec_cache is not None:
        return _spec_cache

    if source is None:
        source = load_config().get("spec_source", DEFAULT_SPEC_URL)

    if source.startswith(("http://", "https://")):
        print(f"Fetching spec from {source} ...")
        raw = _fetch_url(source)
        if source.endswith(".json"):
            _spec_cache = json.loads(raw)
        else:
            _spec_cache = yaml.safe_load(raw)
    else:
        path = Path(source)
        if not path.exists():
            raise RuntimeError(f"Spec file not found: {path}")
        print(f"Loading spec from {path} ...")
        with open(path) as f:
            if path.suffix == ".json":
                _spec_cache = json.load(f)
            else:
                _spec_cache = yaml.safe_load(f)

    return _spec_cache


def load_config() -> dict:
    """Load codegen configuration from ``config.yml``.

    :return: configuration dictionary.
    """
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f) or {}


def to_snake_case(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case.

    :param name: input string.
    :return: snake_case string.
    """
    s = name.replace("-", "_")
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_python_name(name: str) -> str:
    """Convert a parameter name to a valid Python identifier.

    :param name: API parameter name.
    :return: valid Python identifier.
    """
    snake = to_snake_case(name)
    if snake and snake[0].isdigit():
        snake = f"p{snake}"
    if keyword.iskeyword(snake):
        snake = f"{snake}_"
    return snake


def tag_to_module_name(tag: str) -> str:
    """Convert an API tag to a Python module name.

    :param tag: API tag string.
    :return: module name in snake_case.
    """
    return to_snake_case(tag.replace(" ", ""))


def tag_to_class_name(tag: str) -> str:
    """Convert an API tag to a resource class name.

    :param tag: API tag string.
    :return: class name with ``Resource`` suffix.
    """
    return tag.replace(" ", "") + "Resource"
