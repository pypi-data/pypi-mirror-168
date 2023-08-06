from .metadata import DrbMetadata, DrbMetadataResolver


__all__ = [
    'DrbMetadata',
    'DrbMetadataResolver',
]

from . import _version
__version__ = _version.get_versions()['version']
