from typing import Any, List, Tuple

import os
from glob import glob


def resolve_paths(
    parent_dir: str,
    path_pattern: str,
) -> tuple[str, list[str]]:
    search_pattern = os.path.join(parent_dir, path_pattern)
    if os.path.isdir(search_pattern):
        search_pattern = os.path.join(
            search_pattern, "*"
        )  # so we can glob all children
    return (
        search_pattern,
        glob(search_pattern),
    )


def generate_path_pattern(
    path_prefix: str,
    path_pattern: str,
    *args: Any,
) -> str:
    full_pattern = path_prefix + path_pattern

    try:
        return full_pattern.format(*args)
    except IndexError:
        raise Exception(
            "Incompatible path_pattern and args combination. path_pattern=%s, args=%s",
            full_pattern,
            args,
        )
