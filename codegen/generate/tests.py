import shutil
import typing as t
from pathlib import Path

from codegen.formatter import run_ruff
from codegen.spec import (
    group_endpoints_by_tag,
    operation_to_method_name,
    param_default,
    param_python_type,
    resolve_parameter,
    resolve_ref,
    resolve_response_type,
)
from codegen.utils import (
    NON_MODEL_TYPES,
    ROOT,
    env,
    load_config,
    load_spec,
    tag_to_class_name,
    tag_to_module_name,
    to_python_name,
)

TESTS_DIR: Path = ROOT / "tests" / "rest"

PLACEHOLDER_DEFAULTS: t.Dict[str, str] = {
    "str": '""',
    "int": "0",
    "float": "0.0",
    "bool": "False",
}


def _default_value(type_str: str) -> str:
    """Return an empty placeholder literal for a Python type.

    :param type_str: Python type annotation string.
    :return: placeholder value literal.
    """
    if type_str.startswith("t.List["):
        return "[]"
    return PLACEHOLDER_DEFAULTS.get(type_str, '""')


def _schema_to_example(
    schema: dict,
    spec: dict,
    _seen: t.Optional[t.Set[str]] = None,
) -> str:
    """Build a Python literal from a JSON Schema, like Swagger UI does.

    Recursively resolves ``$ref``, ``properties``, ``items``,
    and ``additionalProperties`` to produce a complete example.

    :param schema: JSON Schema dict.
    :param spec: full OpenAPI spec for resolving ``$ref``.
    :param _seen: tracked ``$ref`` paths to prevent circular recursion.
    :return: Python literal string.
    """
    if _seen is None:
        _seen = set()

    if "$ref" in schema:
        ref = schema["$ref"]
        if ref in _seen:
            return "{}"
        _seen = _seen | {ref}
        schema = resolve_ref(ref, spec)

    example = schema.get("example")
    if example is not None:
        return _format_value(example)

    schema_type = schema.get("type", "object")

    if schema_type == "object":
        props = schema.get("properties", {})
        if props:
            parts = []
            for name, prop_schema in props.items():
                val = _schema_to_example(prop_schema, spec, _seen)
                parts.append(f'"{name}": {val}')
            return "{" + ", ".join(parts) + "}"
        additional = schema.get("additionalProperties", {})
        if additional:
            val = _schema_to_example(additional, spec, _seen)
            return "{" + f'"additionalProp1": {val}, "additionalProp2": {val}' + "}"
        return "{}"

    if schema_type == "array":
        items = schema.get("items", {})
        val = _schema_to_example(items, spec, _seen)
        return f"[{val}]"

    if schema_type == "string":
        fmt = schema.get("format", "")
        if fmt == "address":
            return (
                '"0:97264395BD65A255A429B11326C84128B7D70FFED7949ABAE3036D506BA38621"'
            )
        return '""'
    if schema_type == "integer":
        return "0"
    if schema_type == "number":
        return "0.0"
    if schema_type == "boolean":
        return "False"

    return '""'


def _format_value(value: object) -> str:
    """Format a Python value as a literal string.

    :param value: value from OpenAPI spec.
    :return: Python literal string.
    """
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        items = ", ".join(_format_value(v) for v in value)
        return f"[{items}]"
    if isinstance(value, dict):
        parts = [f'"{k}": {_format_value(v)}' for k, v in value.items()]
        return "{" + ", ".join(parts) + "}"
    return str(value)


def _collect_method_info(
    operation: dict,
    spec: dict,
    tag: str,
    overrides: t.Dict[str, str],
) -> dict:
    """Extract method name, required call args, and response type.

    :param operation: OpenAPI operation dictionary.
    :param spec: full OpenAPI spec.
    :param tag: API tag.
    :param overrides: method name overrides.
    :return: dict with ``name``, ``call_args``, ``has_body``, ``body_example``, ``response_type``.
    """
    method_name = operation_to_method_name(
        operation.get("operationId", "unknown"),
        tag,
        overrides,
    )

    raw_params = operation.get("parameters", [])
    params = [resolve_parameter(p, spec) for p in raw_params]

    call_args: t.List[t.Tuple[str, str]] = []

    for p in params:
        if p.get("in") == "path":
            py_name = to_python_name(p["name"])
            ptype = param_python_type(p.get("schema", {}))
            call_args.append((py_name, _default_value(ptype)))

    for p in params:
        if (
            p.get("in") == "query"
            and p.get("required", False)
            and param_default(p) is None
        ):
            py_name = to_python_name(p["name"])
            ptype = param_python_type(p.get("schema", {}))
            call_args.append((py_name, _default_value(ptype)))

    has_body = False
    body_example = "{}"
    if "requestBody" in operation:
        has_body = True
        rb = operation["requestBody"]
        if "$ref" in rb:
            rb = resolve_ref(rb["$ref"], spec)
        content = rb.get("content", {})
        for _, media in content.items():
            schema = media.get("schema", {})
            body_example = _schema_to_example(schema, spec)
            break

    response_type = resolve_response_type(operation, spec)

    return {
        "name": method_name,
        "call_args": call_args,
        "has_body": has_body,
        "body_example": body_example,
        "response_type": response_type,
    }


def run() -> None:
    """Generate all test scaffold files."""
    spec = load_spec()
    config = load_config()
    overrides = config.get("method_names", {})
    skip_tests: t.Set[str] = set(config.get("skip_tests", []))

    tag_endpoints = group_endpoints_by_tag(spec)

    tag_methods: t.Dict[str, t.List[dict]] = {}
    for tag in sorted(tag_endpoints):
        methods = []
        for _, _, operation in tag_endpoints[tag]:
            operation_id = operation.get("operationId", "")
            info = _collect_method_info(
                operation,
                spec,
                tag,
                overrides,
            )
            info["skipped"] = operation_id in skip_tests
            methods.append(info)
        tag_methods[tag] = methods

    total = sum(len(v) for v in tag_methods.values())
    print(f"Found {total} methods across {len(tag_methods)} tags")

    # Preserve fixtures.py (user-edited) across regeneration.
    fixtures_path = TESTS_DIR / "fixtures.py"
    fixtures_backup = None
    if fixtures_path.exists():
        fixtures_backup = fixtures_path.read_text()

    if TESTS_DIR.exists():
        shutil.rmtree(TESTS_DIR)
    TESTS_DIR.mkdir(parents=True)

    # --- Generate fixtures.py ---
    fixtures_entries: t.List[t.Tuple[str, t.List[t.Tuple[str, str]], bool]] = []
    for tag in sorted(tag_methods):
        module = tag_to_module_name(tag)
        for m in tag_methods[tag]:
            if not m["call_args"] and not m["has_body"]:
                continue
            entry_params: t.List[t.Tuple[str, str]] = []
            for arg_name, arg_default in m["call_args"]:
                entry_params.append((arg_name, arg_default))
            if m["has_body"]:
                entry_params.append(("body", m["body_example"]))
            fixtures_entries.append(
                (f"{module}.{m['name']}", entry_params, m["skipped"]),
            )

    fixtures_template = env.get_template("fixtures.py.j2")
    generated_fixtures = fixtures_template.render(entries=fixtures_entries)

    if fixtures_backup is not None:
        (TESTS_DIR / "fixtures.py").write_text(fixtures_backup)
        (TESTS_DIR / "fixtures.py.new").write_text(generated_fixtures)
        print("Preserved fixtures.py (saved new version to fixtures.py.new)")
    else:
        (TESTS_DIR / "fixtures.py").write_text(generated_fixtures)
        print(f"Generated fixtures.py ({len(fixtures_entries)} entries)")

    # --- Generate test modules ---
    test_template = env.get_template("test.py.j2")

    for tag in sorted(tag_methods):
        module = tag_to_module_name(tag)
        class_name = tag_to_class_name(tag)
        methods = tag_methods[tag]

        model_imports: t.Set[str] = set()
        for m in methods:
            if m["response_type"] and m["response_type"] not in NON_MODEL_TYPES:
                model_imports.add(m["response_type"])
            if m["response_type"] == "t.Dict[str, t.Any]":
                m["response_type"] = "dict"

        has_active = any(not m.get("skipped") for m in methods)
        result = test_template.render(
            module_name=module,
            class_name=class_name,
            model_imports=model_imports,
            methods=methods,
            has_active=has_active,
        )
        (TESTS_DIR / f"test_{module}.py").write_text(result)
        print(f"Generated test_{module}.py ({len(methods)} tests)")

    (TESTS_DIR / "__init__.py").write_text(
        "# This file is auto-generated. Do not edit manually.\n",
    )
    print("Generated __init__.py")

    print(f"\nDone! Generated {len(tag_methods)} test modules.")
    run_ruff(TESTS_DIR)
