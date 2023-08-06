from typing import Any, Dict

from ..dataclasses import Template
from .schemas import Template as TemplateSchema

template_schema = TemplateSchema()


def dict_to_template(data: dict[str, Any]) -> Any:
    return template_schema.load(data)


def alt_dict_to_template(data: dict[str, Any]) -> Template:
    """
    Note
    ----
    alternative template syntax from Ben
    """
    path_patterns = []
    for key, value in data["files"].items():
        filename = value.get("filename")
        directory_name = value.get("directory_name")
        if filename:
            path_patterns.append(filename.lstrip("%"))
        elif directory_name:
            path_patterns.append(directory_name.lstrip("%"))
        else:
            raise Exception("Invalid format for: %s" % value)

    return Template(
        name=data["name"],
        path_prefix="{}-{}-{}",
        path_patterns=path_patterns,
    )


def is_alt_format(data: dict[str, Any]) -> bool:
    return data.get("files") is not None
