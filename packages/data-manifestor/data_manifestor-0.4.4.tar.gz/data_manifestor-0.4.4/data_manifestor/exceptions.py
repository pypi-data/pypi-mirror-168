class DataManifestorError(Exception):

    """Base exception type for all data_manifestor errors."""


class PathError(DataManifestorError):

    """An issue related to finding a path."""


class ManifestError(DataManifestorError):

    """An issue related to parsing the manifest."""
