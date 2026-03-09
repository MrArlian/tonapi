import keyword
import re
import typing as t
from collections import defaultdict
from pathlib import Path

from codegen.formatter import run_ruff
from codegen.spec import (
    collect_refs,
    resolve_type,
    resolve_type_for_ref_check,
)
from codegen.utils import (
    ROOT,
    env,
    load_spec,
    tag_to_module_name,
    to_python_name,
)

MODELS_DIR: Path = ROOT / "pytonapi" / "rest" / "models"


def _is_enum_schema(schema: dict) -> bool:
    """Check if schema is a top-level string enum.

    :param schema: component schema dict.
    :return: ``True`` if the schema is a string enum.
    """
    return "enum" in schema and schema.get("type") == "string"


def _is_type_alias_schema(schema: dict) -> bool:
    """Check if schema is a type alias (array or primitive, not object).

    :param schema: component schema dict.
    :return: ``True`` if the schema represents a type alias.
    """
    type_ = schema.get("type")
    if type_ == "array":
        return True
    if type_ in ("string", "integer", "number", "boolean") and "enum" not in schema:
        return True
    return False


def _build_schema_to_module(
        spec: dict,
        schemas: dict,
) -> t.Dict[str, str]:
    """Map each schema name to a target module.

    :param spec: full OpenAPI spec.
    :param schemas: all component schemas.
    :return: mapping of schema name to module name.
    """
    tag_schema_count: t.Dict[str, t.Dict[str, int]] = defaultdict(
        lambda: defaultdict(int),
    )

    for path_item in spec.get("paths", {}).values():
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            tags = operation.get("tags", [])
            direct_refs = collect_refs(operation)
            for tag in tags:
                module = tag_to_module_name(tag)
                for ref in direct_refs:
                    if ref in schemas:
                        tag_schema_count[module][ref] += 1

    schema_to_module: t.Dict[str, str] = {}
    for schema_name in schemas:
        best_module = None
        best_count = 0
        for module, counts in tag_schema_count.items():
            c = counts.get(schema_name, 0)
            if c > best_count:
                best_count = c
                best_module = module
        if best_module:
            schema_to_module[schema_name] = best_module

    changed = True
    while changed:
        changed = False
        unassigned = set(schemas.keys()) - set(schema_to_module.keys())
        if not unassigned:
            break
        ref_from: t.Dict[str, t.Dict[str, int]] = defaultdict(
            lambda: defaultdict(int),
        )
        for name in schema_to_module:
            parent_module = schema_to_module[name]
            for ref in collect_refs(schemas.get(name, {})):
                if ref in unassigned:
                    ref_from[ref][parent_module] += 1
        for name in list(unassigned):
            if name in ref_from:
                best = max(ref_from[name], key=ref_from[name].get)
                schema_to_module[name] = best
                changed = True

    all_modules = sorted(tag_schema_count.keys()) if tag_schema_count else ["common"]
    for name in set(schemas.keys()) - set(schema_to_module.keys()):
        schema_to_module[name] = all_modules[0]

    return schema_to_module


def _sanitize_enum_member(value: str) -> str:
    """Make an enum value a valid Python identifier.

    :param value: raw enum string value.
    :return: valid Python identifier.
    """
    v = value
    if v and v[0].isdigit():
        v = f"_{v}"
    v = re.sub(r"[^a-zA-Z0-9_]", "_", v)
    if keyword.iskeyword(v):
        v = f"{v}_"
    if not v:
        v = "_empty"
    return v


def _needs_alias(original: str, python_name: str) -> bool:
    """Check if a field needs an alias.

    :param original: original API field name.
    :param python_name: converted Python name.
    :return: ``True`` if alias is needed.
    """
    return original != python_name


def _generate_field(
        field_name: str,
        prop: dict,
        required: bool,
        schemas: dict,
        enum_names: t.Set[str],
) -> str:
    """Generate a single model field line.

    :param field_name: original API field name.
    :param prop: property schema.
    :param required: whether the field is required.
    :param schemas: all component schemas.
    :param enum_names: known enum schema names.
    :return: field definition line.
    """
    type_str = resolve_type(prop, schemas, enum_names)
    python_name = to_python_name(field_name)
    alias_needed = _needs_alias(field_name, python_name)

    is_optional = not required or prop.get("nullable", False)
    if is_optional:
        type_str = f"t.Optional[{type_str}]"

    parts: t.List[str] = []
    if alias_needed:
        parts.append(f'alias="{field_name}"')
    if is_optional:
        parts.append("default=None")

    if parts:
        field_args = ", ".join(parts)
        return f"{python_name}: {type_str} = Field({field_args})"
    return f"{python_name}: {type_str}"


def _collect_model_refs(schema: dict) -> t.Set[str]:
    """Collect all ``$ref`` model names from a schema's properties.

    :param schema: component schema dict.
    :return: set of referenced model names.
    """
    refs: t.Set[str] = set()
    for prop in schema.get("properties", {}).values():
        refs |= resolve_type_for_ref_check(prop)
    return refs


def _topological_sort(
        models: t.Dict[str, dict],
        schema_to_module: t.Dict[str, str],
        module: str,
) -> t.List[str]:
    """Sort models within a module so dependencies come first.

    :param models: all model schemas.
    :param schema_to_module: schema-to-module mapping.
    :param module: target module name.
    :return: ordered list of schema names.
    """
    local = {
        n for n, m in schema_to_module.items()
        if m == module and n in models
    }
    order: t.List[str] = []
    visited: t.Set[str] = set()
    in_progress: t.Set[str] = set()

    def visit(name: str) -> None:
        if name in visited or name not in local:
            return
        if name in in_progress:
            return
        in_progress.add(name)
        for ref in _collect_model_refs(models[name]):
            if ref in local:
                visit(ref)
        in_progress.discard(name)
        visited.add(name)
        order.append(name)

    for name in sorted(local):
        visit(name)
    return order


def _build_module_context(
        module: str,
        schemas: dict,
        schema_to_module: t.Dict[str, str],
        enum_names: t.Set[str],
) -> t.Optional[dict]:
    """Build template context for a single model module.

    :param module: target module name.
    :param schemas: all component schemas.
    :param schema_to_module: schema-to-module mapping.
    :param enum_names: known enum schema names.
    :return: template context dict, or ``None`` if module is empty.
    """
    type_alias_schemas: t.Dict[str, dict] = {}
    model_schemas: t.Dict[str, dict] = {}
    for n in schemas:
        if schema_to_module.get(n) != module or n in enum_names:
            continue
        if _is_type_alias_schema(schemas[n]):
            type_alias_schemas[n] = schemas[n]
        else:
            model_schemas[n] = schemas[n]

    if not model_schemas and not type_alias_schemas:
        return None

    ordered = _topological_sort(model_schemas, schema_to_module, module)
    type_alias_names = sorted(type_alias_schemas.keys())

    enum_imports: t.Set[str] = set()
    type_checking_cross: t.Dict[str, t.Set[str]] = defaultdict(set)

    for name in ordered:
        for ref in _collect_model_refs(schemas[name]):
            if ref in enum_names:
                enum_imports.add(ref)
            elif schema_to_module.get(ref, module) != module:
                ref_module = schema_to_module[ref]
                type_checking_cross[ref_module].add(ref)

    needs_config_dict = False
    for name in ordered:
        props = schemas[name].get("properties", {})
        if any(_needs_alias(fn, to_python_name(fn)) for fn in props):
            needs_config_dict = True
            break

    needs_pydantic = bool(model_schemas)

    pydantic_imports: t.List[str] = []
    if needs_pydantic:
        pydantic_imports = ["BaseModel", "Field"]
        if needs_config_dict:
            pydantic_imports.append("ConfigDict")

    definitions: t.List[dict] = []

    for name in type_alias_names:
        type_str = resolve_type(schemas[name], schemas, enum_names)
        definitions.append({
            "kind": "alias",
            "name": name,
            "type_str": type_str,
        })

    for name in ordered:
        schema = schemas[name]
        if _is_enum_schema(schema):
            continue

        required_set = set(schema.get("required", []))
        properties = schema.get("properties", {})

        required_fields: t.List[str] = []
        optional_fields: t.List[str] = []
        for field_name, prop in properties.items():
            is_req = field_name in required_set and not prop.get("nullable", False)
            line = _generate_field(
                field_name, prop, field_name in required_set, schemas, enum_names,
            )
            if is_req:
                required_fields.append(line)
            else:
                optional_fields.append(line)

        has_alias = any(
            _needs_alias(fn, to_python_name(fn)) for fn in properties
        )

        definitions.append({
            "kind": "model",
            "name": name,
            "fields": required_fields + optional_fields,
            "has_alias": has_alias,
        })

    tc_imports = [
        (mod, sorted(names))
        for mod, names in sorted(type_checking_cross.items())
    ]

    return {
        "needs_pydantic": needs_pydantic,
        "pydantic_imports": pydantic_imports,
        "enum_imports": enum_imports,
        "type_checking_imports": tc_imports,
        "definitions": definitions,
    }


def run() -> None:
    """Generate all model files."""
    spec = load_spec()
    schemas = spec["components"]["schemas"]
    print(f"Loaded {len(schemas)} schemas")

    enum_names = {n for n in schemas if _is_enum_schema(schemas[n])}
    print(f"Found {len(enum_names)} enums")

    schema_to_module = _build_schema_to_module(spec, schemas)

    module_counts: t.Dict[str, int] = defaultdict(int)
    for module in schema_to_module.values():
        module_counts[module] += 1
    for mod in sorted(module_counts):
        print(f"  {mod}: {module_counts[mod]} schemas")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # _enums.py
    enums_data: t.List[dict] = []
    for name in sorted(schemas):
        if _is_enum_schema(schemas[name]):
            members = [
                (_sanitize_enum_member(v), v)
                for v in schemas[name]["enum"]
            ]
            enums_data.append({"name": name, "members": members})

    template = env.get_template("enums.py.j2")
    (MODELS_DIR / "_enums.py").write_text(template.render(enums=enums_data))
    print("Generated _enums.py")

    # Module files
    modules_generated: t.Set[str] = set()
    template = env.get_template("model.py.j2")

    for module in sorted(set(schema_to_module.values())):
        ctx = _build_module_context(module, schemas, schema_to_module, enum_names)
        if ctx is None:
            continue

        code = template.render(**ctx)
        (MODELS_DIR / f"{module}.py").write_text(code)
        count = sum(
            1 for n, m in schema_to_module.items()
            if m == module and n not in enum_names
        )
        print(f"Generated {module}.py ({count} models)")
        modules_generated.add(module)

    # __init__.py
    type_alias_names = {n for n in schemas if _is_type_alias_schema(schemas[n])}
    module_to_names: t.Dict[str, t.List[str]] = defaultdict(list)
    for name, module in sorted(schema_to_module.items()):
        module_to_names[module].append(name)

    module_imports: t.List[t.Tuple[str, t.List[str]]] = []
    for module in sorted(module_to_names):
        names = [
            n for n in sorted(module_to_names[module])
            if n not in enum_names
        ]
        if names:
            module_imports.append((module, names))

    rebuild_models: t.List[str] = []
    for module in sorted(module_to_names):
        names = [
            n for n in sorted(module_to_names[module])
            if n not in enum_names and n not in type_alias_names
        ]
        rebuild_models.extend(names)

    all_names = [f'"{n}"' for n in sorted(schema_to_module.keys())]

    init_template = env.get_template("model_init.py.j2")
    init_code = init_template.render(
        enum_names=sorted(enum_names),
        module_imports=module_imports,
        rebuild_models=rebuild_models,
        all_names=all_names,
    )
    (MODELS_DIR / "__init__.py").write_text(init_code)
    print("Generated __init__.py")

    print(
        f"\nDone! Generated {len(schemas)} schemas "
        f"across {len(modules_generated)} modules.",
    )
    run_ruff(MODELS_DIR)
