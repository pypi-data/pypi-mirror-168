import json
import os
import sys
import textwrap
from typing import cast

from glom import glom  # type: ignore
from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel

from . import validators

template_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_dir))

SETTINGS = {
    "hcl": {
        "template": cast(Template, env.get_template("hcl.tf")),
        "delimiter": "\n\n",
    },
    "tfvars": {
        "template": cast(Template, env.get_template("variable.tfvars")),
        "delimiter": "\n",
    },
    "module": {
        "template": cast(Template, env.get_template("module_params.tf")),
        "delimiter": "\n",
        "wrapper": cast(Template, env.get_template("module_wrapper.tf")),
    },
}


class Converter:

    numbers = ["int", "float", "integer"]
    objects = ["dict", "object"]
    pass_through_fields = ["string"]

    def __init__(self, format="hcl") -> None:
        if format not in SETTINGS:
            raise ValueError(f"Format must be hcl or tfvars")
        self.template = SETTINGS[format]["template"]
        self.delimiter = SETTINGS[format]["delimiter"]
        self.wrapper = cast(Template, SETTINGS[format]["wrapper"]) if "wrapper" in SETTINGS[format] else None

    def convert(self, model: BaseModel) -> str:
        schema = model.schema()
        output = ""
        for field_name, field_data in schema["properties"].items():
            output += self.convert_field(schema, field_name, field_data)
            output += self.delimiter  # type: ignore

        if self.wrapper:
            output = self.wrapper.render(parameters=output)

        return output.strip()

    def _get_reference(self, schema, reference):
        # Convert reference into glom format.
        path = reference.strip("#/").replace("/", ".")
        return glom(schema, path)

    def convert_field(self, schema, field_name, field_data) -> str:

        # This field references another field. Swap the field_data out.
        if "$ref" in field_data:
            field_data = self._get_reference(schema, field_data["$ref"])

        if "allOf" in field_data:
            for parent_model in field_data["allOf"]:
                if "$ref" in parent_model:
                    parent_model = self._get_reference(schema, parent_model["$ref"])
                field_data |= parent_model

        type, type_rules = self.get_type(field_name, field_data)

        rules = self.get_validation_list(field_name, field_data)
        if type_rules:
            rules += type_rules

        # Since "null" and "false" are valid defaults we can't rely on default being defined.
        # To get around that we have `has_default`.
        has_default = False
        default = None
        if "default" in field_data or field_name not in schema["required"]:
            has_default = True
            default = self.get_default(type, field_data.get("default"))

        return self.template.render(  # type: ignore
            name=field_name,
            type=type,
            description=field_data.get("description"),
            has_default=has_default,
            default=default,
            validation_rules=rules,
        )

    def get_type(self, field_name, field_data):

        if "type" not in field_data:
            if "enum" in field_data:
                return "string", [validators.oneof(field_name, field_data["enum"])]
            print(field_data)
            raise ValueError(f"Unknown type for {field_name}")

        field_type = field_data["type"].lower()

        if field_type in self.pass_through_fields:
            return field_type, None

        if field_type in self.numbers:
            return "number", None

        if field_type == "array":
            subtype = self.get_subtype(field_name, field_data)
            return f"list({subtype})", None

        if field_type in self.objects:
            subtype = self.get_subtype(field_name, field_data)
            return f"map({subtype})", None

        if field_type == "boolean":
            return "bool", None

        return "string", None

    def get_subtype(self, field_name, field_data):
        subtype = "any"
        if "items" in field_data:
            if "type" in field_data["items"]:
                subtype, rules = self.get_type(field_name, field_data["items"])
        if "additionalProperties" in field_data and "type" in field_data["additionalProperties"]:
            subtype = field_data["additionalProperties"]["type"]
        return subtype

    def get_default(self, type, value):
        if type.startswith("list"):
            return textwrap.indent(json.dumps(value, indent=2), "  ").strip() if value else "[]"
        if type.startswith("map"):
            return textwrap.indent(json.dumps(value, indent=2), "  ").strip() if value else "{}"

        # Custom Nulls above this line

        if value == None:
            return "null"
        if type == "number":
            return value
        if type == "string":
            escaped_value = str(value).replace('"', '\\"')
            return f'"{escaped_value}"'
        if type == "bool":
            return "true" if value else "false"

        return "null"

    def get_validation_list(self, field_name, field_data):
        tf_rules = []
        for key, value in field_data.items():
            if not hasattr(validators, key.lower()):
                continue
            rule = getattr(validators, key.lower())(field_name, value)
            if rule:
                tf_rules.append(rule)

        return tf_rules
