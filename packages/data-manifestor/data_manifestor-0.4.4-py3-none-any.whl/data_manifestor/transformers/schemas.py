from typing import Any, Dict

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_load,
    validate,
    validates_schema,
)

from .. import dataclasses


class Template(Schema):

    __model__ = dataclasses.Template

    name = fields.String()
    path_prefix = fields.String(dump_default="{}-{}-{}")
    path_patterns = fields.List(fields.String())

    @post_load
    def make_dataclass(self, data: dict[str, Any], **kwargs: Any) -> Any:
        return self.__model__(**data)
