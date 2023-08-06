from __future__ import annotations

import os
import jsonschema
import yaml
import importlib
import logging

from importlib.metadata import entry_points
from types import ModuleType
from typing import Any, Dict, List, Tuple
from uuid import UUID
from drb import DrbNode
from drb.factory import ItemClass, ItemClassLoader, DrbFactoryResolver
from drb.exceptions import DrbException


from .extractor import Extractor, parse_extractor


_logger = logging.getLogger('DrbMetadata')
_schema = os.path.join(os.path.dirname(__file__), 'schema.yml')


def validate_md_cortex_file(path: str) -> None:
    """
    Checks the given metadata cortex file is valid.

    Parameters:
        path (str): metadata cortex file path

    Raises:
        DrbException: If the given cortex file is not valid
    """
    with open(_schema) as f:
        schema = yaml.safe_load(f)

    with open(path) as file:
        for data in yaml.safe_load_all(file):
            try:
                jsonschema.validate(data, schema)
            except jsonschema.ValidationError as ex:
                raise DrbException(
                    f'Invalid metadata cortex file: {path}') from ex


def _retrieve_cortex_file(module: ModuleType) -> str:
    """
    Retrieves the metadata cortex file from the given module.

    Parameters:
        module (ModuleType): target module where the cortex metadata file will
                             be search
    Returns:
        str - path to the cortex metadata file
    Raises:
        FileNotFound: If the metadata cortex file is not found
    """
    directory = os.path.dirname(module.__file__)
    path = os.path.join(directory, 'cortex.yml')
    if not os.path.exists(path):
        path = os.path.join(directory, 'cortex.yaml')

    if not os.path.exists(path):
        raise FileNotFoundError(f'File not found: {path}')

    return path


def _load_metadata(yaml_data: dict) -> Tuple[UUID, List[DrbMetadata]]:
    uuid = UUID(yaml_data['drbItemClass'])

    variables = {}
    yaml_vars = yaml_data.get('variables', None)
    if yaml_vars is not None:
        for var in yaml_vars:
            extractor = parse_extractor(var)
            variables[var['name']] = extractor

    metadata = []
    for md in yaml_data['metadata']:
        extractor = parse_extractor(md)
        metadata.append(DrbMetadata(md['name'], extractor, variables))
    return uuid, metadata


def _load_all_metadata() -> Dict[UUID, List[DrbMetadata]]:
    """
    Loads all metadata defined in the current Python environment
    """
    entry_point_group = 'drb.metadata'
    metadata = {}

    eps = entry_points()
    if entry_point_group not in eps:
        _logger.warning('No DRB Metadata found')
        return metadata

    for ep in eps[entry_point_group]:
        try:
            module = importlib.import_module(ep.value)
        except ModuleNotFoundError as ex:
            _logger.warning(f'Invalid DRB Metadata entry-point {ep}: {ex.msg}')
            continue

        try:
            cortex = _retrieve_cortex_file(module)
            validate_md_cortex_file(cortex)
        except (FileNotFoundError, DrbException) as ex:
            _logger.warning(ex)
            continue

        with open(cortex) as file:
            for data in yaml.safe_load_all(file):
                uuid, mds = _load_metadata(data)
                metadata[uuid] = mds

    return metadata


class DrbMetadata:
    def __init__(self, name: str, extractor: Extractor,
                 variables: dict = None):
        self._name = name
        self._extractor = extractor
        self._variables = variables if variables is not None else {}

    @property
    def name(self) -> str:
        return self._name

    def extract(self, node: DrbNode) -> Any:
        variables = {}
        for name, extractor in self._variables.items():
            variables[name] = extractor.extract(node, **variables)
        return self._extractor.extract(node, **variables)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DrbMetadata) and self._name == other._name


class DrbMetadataResolver:
    __instance = None
    __ic_loader: ItemClassLoader = None
    __metadata: Dict[UUID, List[DrbMetadata]] = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DrbMetadataResolver, cls).__new__(cls)
            cls.__ic_loader = ItemClassLoader()
            cls.__metadata = _load_all_metadata()
        return cls.__instance

    def _retrieve_metadata(self, ic: ItemClass) -> Dict[str, DrbMetadata]:
        metadata = None

        # load metadata from super class
        if ic.parent_class_id is not None:
            parent = self.__ic_loader.get_item_class(ic.parent_class_id)
            metadata = self._retrieve_metadata(
                self.__ic_loader.get_item_class(parent.id))

        if metadata is None:
            metadata = {}

        # add specific metadata of the given class (override if necessary)
        if ic.id in self.__metadata.keys():
            for md in self.__metadata[ic.id]:
                metadata[md.name] = md

        return metadata

    def get_metadata(self, node: DrbNode) -> Dict[str, DrbMetadata]:
        ic, base_node = DrbFactoryResolver().resolve(node)
        return self._retrieve_metadata(ic)
