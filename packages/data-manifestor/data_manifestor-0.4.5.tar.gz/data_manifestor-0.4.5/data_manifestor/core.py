from typing import Any, Dict, Optional, Tuple

import logging
import os
from glob import glob

from np_lims_tk.core import get_project_name, project_name_to_data_manifestor_template
from np_lims_tk.local_paths import path_to_lims_meta

from .dataclasses import LocalComparisonResult, Manifest
from .exceptions import ManifestError, PathError
from .paths import generate_path_pattern, resolve_paths
from .transformers import alt_dict_to_template, dict_to_template, is_alt_format

logger = logging.getLogger(__name__)


def generate_manifest(template_dict: dict[str, Any], *args: str) -> Manifest:
    try:
        if is_alt_format(template_dict):
            template = alt_dict_to_template(template_dict)
        else:
            template = dict_to_template(template_dict)

        path_patterns = [
            generate_path_pattern(template.path_prefix, path_pattern, *args)
            for path_pattern in template.path_patterns
        ]
    except Exception as e:
        raise ManifestError("Error parsing manifest") from e

    return Manifest(
        name=template.name,
        template=template,
        args=args,
        path_patterns=path_patterns,
    )


def compare_manifest_to_local(
    local_dir: str,
    *args: str,
    template_dict: Optional[dict[str, Any]] = None,
) -> LocalComparisonResult:
    if not template_dict:
        logger.debug("Autogenerating manifest and args")
        template_dict, args = path_to_manifest_template(local_dir)
        if not template_dict:
            raise ManifestError("Couldnt infer template from path. path=%s" % local_dir)

    manifest = generate_manifest(template_dict, *args)
    resolved_paths = []
    found = []
    missing = []
    for path_pattern in manifest.path_patterns:
        pattern, paths = resolve_paths(local_dir, path_pattern)
        if len(paths) > 0:
            found.extend(paths)
        else:
            missing.append(pattern)
        resolved_paths.append(
            (
                pattern,
                paths,
            )
        )
    return LocalComparisonResult(
        local_dir=local_dir,
        manifest=manifest,
        resolved_paths=resolved_paths,
        found=found,
        missing=missing,
    )


def path_to_manifest_template(path: str) -> tuple[Any, tuple[Any, ...]]:
    """Infers associated manifest template from a file or directory path.

    Args
    ----
    path: File or directory path.

    Returns
    -------
    manifest template and necessary arguments associated with it

    Raises
    ------
    ManifestError
    - An unexpected error occurred
    """
    try:
        lims_meta = path_to_lims_meta(path)
        logger.debug("Resolved lims meta: %s" % lims_meta)
        lims_id = lims_meta._id
        subject_id = lims_meta.subject_id
        date_str = lims_meta.date_str
        project_name = get_project_name(lims_id=lims_id)
        logger.debug("Resolved project name: %s" % project_name)
        return project_name_to_data_manifestor_template(project_name), (
            lims_id,
            subject_id,
            date_str,
        )
    except Exception as e:
        raise ManifestError("Error parsing manifest") from e
