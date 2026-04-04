from __future__ import annotations

import re
import typing as t

if t.TYPE_CHECKING:
    from pathlib import Path

from codegen.spec import group_endpoints_by_tag
from codegen.utils import ROOT, env, load_spec, to_snake_case

DOCS_REST_DIR: Path = ROOT / "docs" / "rest"
DOCS_JSON_PATH: Path = ROOT / "docs" / "docs.json"


def _operation_id_to_title(operation_id: str) -> str:
    """Convert camelCase operationId to human-readable title.

    :param operation_id: camelCase operation identifier.
    :return: human-readable title string.
    """
    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", operation_id)
    words = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", words)
    return words.title()


def _update_docs_json(name_mapping: dict[str, str]) -> None:
    """Update ``docs.json`` navigation to use snake_case page references.

    :param name_mapping: mapping from old camelCase ref to new snake_case ref.
    """
    if not DOCS_JSON_PATH.exists():
        return

    text = DOCS_JSON_PATH.read_text()
    for old_ref, new_ref in name_mapping.items():
        text = text.replace(f'"rest/{old_ref}"', f'"rest/{new_ref}"')
    DOCS_JSON_PATH.write_text(text)
    print(f"Updated docs.json ({len(name_mapping)} page references)")


def run() -> None:
    """Generate endpoint ``.mdx`` files in ``docs/rest/``."""
    spec = load_spec()
    tag_endpoints = group_endpoints_by_tag(spec)
    template = env.get_template("endpoint.mdx.j2")

    DOCS_REST_DIR.mkdir(parents=True, exist_ok=True)

    name_mapping: dict[str, str] = {}
    count = 0
    for tag in sorted(tag_endpoints):
        for path, http_method, operation in tag_endpoints[tag]:
            operation_id = operation.get("operationId")
            if not operation_id:
                continue

            title = operation.get("summary") or _operation_id_to_title(operation_id)
            snake_name = to_snake_case(operation_id)
            filename = f"{snake_name}_{http_method}.mdx"

            old_ref = f"{operation_id}_{http_method}"
            new_ref = f"{snake_name}_{http_method}"
            if old_ref != new_ref:
                name_mapping[old_ref] = new_ref

            result = template.render(
                title=title,
                http_method=http_method.upper(),
                path=path,
            )
            (DOCS_REST_DIR / filename).write_text(result)
            count += 1

    print(f"Generated {count} endpoint .mdx files in docs/rest/")
    _update_docs_json(name_mapping)
