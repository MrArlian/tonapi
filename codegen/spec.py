import typing as t
from collections import defaultdict

from codegen.utils import TYPE_MAP, to_snake_case


def ref_name(ref_path: str) -> str:
    """Extract the schema name from a ``$ref`` path.

    :param ref_path: JSON pointer like ``#/components/schemas/Foo``.
    :return: schema name (e.g. ``Foo``).
    """
    return ref_path.split("/")[-1]


def resolve_ref(ref_path: str, spec: dict) -> dict:
    """Follow a ``$ref`` path and return the resolved object.

    :param ref_path: JSON pointer string like ``#/components/schemas/Foo``.
    :param spec: full OpenAPI spec dictionary.
    :return: resolved schema or parameter object.
    :raises KeyError: if the path does not exist in the spec.
    """
    obj = spec
    parts = ref_path.split("/")[1:]
    for i, part in enumerate(parts):
        if not isinstance(obj, dict) or part not in obj:
            traversed = "/".join(parts[:i])
            raise KeyError(
                f"Cannot resolve $ref '{ref_path}': "
                f"key '{part}' not found at '#{traversed}'"
            )
        obj = obj[part]
    return obj


def resolve_parameter(param: dict, spec: dict) -> dict:
    """Resolve a parameter, following ``$ref`` if needed.

    :param param: parameter dict, possibly containing ``$ref``.
    :param spec: full OpenAPI spec dictionary.
    :return: resolved parameter dictionary.
    """
    if "$ref" in param:
        return resolve_ref(param["$ref"], spec)
    return param


def param_python_type(schema: dict) -> str:
    """Convert a parameter schema to a Python type string.

    :param schema: JSON Schema for the parameter.
    :return: Python type annotation string.
    """
    type_ = schema.get("type", "string")
    if type_ == "array":
        items_type = TYPE_MAP.get(
            schema.get("items", {}).get("type", "string"),
            "str",
        )
        return f"t.List[{items_type}]"
    return TYPE_MAP.get(type_, "str")


def param_default(param: dict) -> t.Optional[str]:
    """Extract the default value literal for a parameter.

    :param param: resolved parameter dictionary.
    :return: Python literal string, or ``None`` if no default.
    """
    schema = param.get("schema", {})
    if "default" in schema:
        val = schema["default"]
        if isinstance(val, bool):
            return str(val)
        if isinstance(val, str):
            return f'"{val}"'
        return str(val)
    return None


def resolve_response_type(
    operation: dict,
    spec: dict,
) -> t.Optional[str]:
    """Determine the response model name from a ``200`` response.

    :param operation: OpenAPI operation dictionary.
    :param spec: full OpenAPI spec dictionary.
    :return: model class name, Python type name, or ``None``.
    """
    resp_200 = operation.get("responses", {}).get("200", {})
    content = resp_200.get("content", {})
    if not content:
        return None

    if "application/json" in content:
        media = content["application/json"]
    else:
        ct, media = next(iter(content.items()))
        schema = media.get("schema", {})
        if schema.get("format") == "binary":
            return "bytes" if ct == "application/octet-stream" else "str"
        return "t.Dict[str, t.Any]"

    schema = media.get("schema", {})
    if "$ref" in schema:
        return ref_name(schema["$ref"])
    type_name = schema.get("type")
    if type_name in TYPE_MAP:
        return TYPE_MAP[type_name]
    return "t.Dict[str, t.Any]"


def operation_to_method_name(
    operation_id: str,
    tag: str,
    overrides: t.Dict[str, str],
) -> str:
    """Convert an ``operationId`` to a Python method name.

    :param operation_id: OpenAPI operationId.
    :param tag: API tag the operation belongs to.
    :param overrides: custom operationId to method name mappings.
    :return: clean Python method name.
    """
    if operation_id in overrides:
        return overrides[operation_id]
    name = to_snake_case(operation_id)
    tag_prefix = to_snake_case(tag.replace(" ", "")) + "_"
    if name.startswith(tag_prefix):
        name = name[len(tag_prefix) :]
    for prefix in ("get_", "send_", "exec_"):
        combined = prefix + tag_prefix
        if name.startswith(combined):
            name = prefix + name[len(combined) :]
            break
    return name


def collect_refs(obj: object) -> t.Set[str]:
    """Recursively collect all ``$ref`` schema names from a schema.

    :param obj: schema object to scan.
    :return: set of referenced schema names.
    """
    refs: t.Set[str] = set()
    if isinstance(obj, dict):
        if "$ref" in obj:
            refs.add(ref_name(obj["$ref"]))
        for v in obj.values():
            refs |= collect_refs(v)
    elif isinstance(obj, list):
        for item in obj:
            refs |= collect_refs(item)
    return refs


def resolve_type(
    prop: dict,
    schemas: dict,
    enum_names: t.Set[str],
) -> str:
    """Resolve an OpenAPI property to a Python type string.

    :param prop: property schema.
    :param schemas: all component schemas.
    :param enum_names: set of known enum schema names.
    :return: Python type annotation string.
    """
    if "allOf" in prop:
        for sub in prop["allOf"]:
            if "$ref" in sub:
                return ref_name(sub["$ref"])
        if prop["allOf"]:
            return resolve_type(prop["allOf"][0], schemas, enum_names)
        return "t.Any"

    if "$ref" in prop:
        return ref_name(prop["$ref"])

    type_ = prop.get("type", "object")

    if type_ == "array":
        items = prop.get("items", {})
        if items.get("type") == "object" and "properties" in items:
            return "t.List[t.Any]"
        if "enum" in items and items.get("type") == "string":
            return "t.List[str]"
        inner = resolve_type(items, schemas, enum_names)
        return f"t.List[{inner}]"

    if type_ == "object":
        additional = prop.get("additionalProperties")
        if isinstance(additional, dict):
            val_type = resolve_type(additional, schemas, enum_names)
            return f"t.Dict[str, {val_type}]"
        if additional:
            return "t.Dict[str, t.Any]"
        return "t.Any"

    if "enum" in prop:
        return "str"

    return TYPE_MAP.get(type_, "t.Any")


def resolve_type_for_ref_check(prop: dict) -> t.Set[str]:
    """Collect all referenced model names from a property.

    :param prop: property schema.
    :return: set of referenced model class names.
    """
    refs: t.Set[str] = set()
    if "$ref" in prop:
        refs.add(ref_name(prop["$ref"]))
    if "allOf" in prop:
        for sub in prop["allOf"]:
            refs |= resolve_type_for_ref_check(sub)
    if "items" in prop:
        refs |= resolve_type_for_ref_check(prop["items"])
    if "additionalProperties" in prop and isinstance(
        prop["additionalProperties"],
        dict,
    ):
        refs |= resolve_type_for_ref_check(prop["additionalProperties"])
    return refs


def group_endpoints_by_tag(
    spec: dict,
) -> t.Dict[str, t.List[t.Tuple[str, str, dict]]]:
    """Group all API endpoints by their tags.

    Endpoints with multiple tags are added to every tag group.

    :param spec: full OpenAPI spec dictionary.
    :return: mapping of tag name to list of ``(path, method, operation)`` tuples.
    """
    tag_endpoints: t.Dict[str, t.List[t.Tuple[str, str, dict]]] = defaultdict(list)
    for path, path_item in spec.get("paths", {}).items():
        for http_method, operation in path_item.items():
            if not isinstance(operation, dict):
                continue
            for tag in operation.get("tags", []):
                tag_endpoints[tag].append((path, http_method, operation))
    return dict(tag_endpoints)
