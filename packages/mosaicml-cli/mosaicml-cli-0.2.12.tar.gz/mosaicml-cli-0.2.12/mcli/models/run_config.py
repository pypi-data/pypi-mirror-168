""" Run Input """
from __future__ import annotations

import logging
import warnings
from dataclasses import asdict, dataclass, field, fields
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from mcli.api.exceptions import MAPIException, MCLIRunConfigValidationError
from mcli.api.schema.generic_model import DeserializableModel
from mcli.models.mcli_cluster import MCLICluster
from mcli.serverside.clusters.cluster_instances import (IncompleteInstanceRequest, InstanceRequest,
                                                        UserInstanceRegistry, ValidInstance)
from mcli.utils.utils_config import uuid_generator
from mcli.utils.utils_string_functions import (ensure_rfc1123_compatibility, snake_case_to_camel_case, validate_image,
                                               validate_rfc1123_name)
from mcli.utils.utils_yaml import load_yaml

logger = logging.getLogger(__name__)
RUN_CONFIG_UID_LENGTH = 4
DEFAULT_OPTIMIZATION_LEVEL = 1
VALID_OPTIMIZATION_LEVELS = frozenset([0, 1, 2])


@dataclass
class FinalRunConfig(DeserializableModel):
    """A finalized run configuration

    This configuration must be complete, with enough details to submit a new run to the
    MosaicML Cloud.
    """

    run_id: str
    name: str
    gpu_type: str
    gpu_num: int
    cpus: int
    image: str
    integrations: List[Dict[str, Any]]
    env_variables: List[Dict[str, str]]

    parameters: Dict[str, Any]

    # Make both optional for initial rollout
    # Eventually make entrypoint required and deprecate command
    optimization_level: int = 0
    command: str = ''
    entrypoint: str = ''

    # Platform is deprecated, but not required for backwards compatibility
    cluster: str = ''
    platform: str = ''

    _property_translations = {
        'run_id': 'run_id',
        'runName': 'name',
        'gpuType': 'gpu_type',
        'gpuNum': 'gpu_num',
        'cpus': 'cpus',
        'cluster': 'cluster',
        'image': 'image',
        'optimizationLevel': 'optimization_level',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'entrypoint': 'entrypoint',
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    def __post_init__(self):
        self.cluster = self.cluster or self.platform

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FinalRunConfig:
        missing = set(cls._property_translations) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=
                f'Missing required key(s) in response to deserialize FinalRunConfig object: {", ".join(missing)}',
            )
        data = {v: response[k] for k, v in cls._property_translations.items()}
        return cls(**data)

    @classmethod
    def finalize_config(cls, run_config: RunConfig) -> FinalRunConfig:
        """Create a :class:`~mcli.models.run_config.FinalRunConfig` from the provided
        :class:`~mcli.models.run_config.RunConfig`.

        If the :class:`~mcli.models.run_config.RunConfig` is not fully populated then
        this function fails with an error.

        Args:
            run_config (:class:`~mcli.models.run_config.RunConfig`): The RunConfig to finalize

        Returns:
            :class:`~mcli.models.run_config.FinalRunConfig`: The object created using values from the input

        Raises:
            :class:`~mcli.api.exceptions.MCLIConfigError`: If MCLI config is not present or is missing information
            :class:`~mcli.api.exceptions.MCLIRunConfigValidationError`: If run_config is not valid
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.config import MCLIConfig
        conf = MCLIConfig.load_config(safe=True)

        if run_config.cpus is None:
            run_config.cpus = 0

        if run_config.optimization_level is None:
            # TODO: not all docker images will support adding the MosaicML Agent
            # If you change the default optimization level for all users, make
            # sure the hello world documentation (image: bash) still works
            run_config.optimization_level = 0

            # Internal composer runs are forced to use default optimization
            if conf.internal:
                run_config.optimization_level = DEFAULT_OPTIMIZATION_LEVEL

        if run_config.cluster:
            _validate_cluster_exists(run_config.cluster)

        if not all((
                run_config.cluster,
                run_config.gpu_type,
                run_config.gpu_num is not None,
        )):
            # Try to infer values from provided
            request = InstanceRequest(cluster=run_config.cluster,
                                      gpu_type=run_config.gpu_type,
                                      gpu_num=run_config.gpu_num)
            logger.debug(f'Incomplete instance request: {request}')
            user_instances = UserInstanceRegistry()
            options = user_instances.lookup(request)
            if len(options) == 1:
                valid_instance = options[0]
                logger.debug(f'Inferred a valid instance request: {valid_instance}')
                run_config.cluster = valid_instance.cluster
                run_config.gpu_type = valid_instance.gpu_type
                run_config.gpu_num = valid_instance.gpu_num
            else:
                valid_registry = ValidInstance.to_registry(options)
                incomplete_instance_error = IncompleteInstanceRequest(
                    requested=request,
                    options=valid_registry,
                    registry=user_instances.registry,
                )
                raise MCLIRunConfigValidationError(str(incomplete_instance_error))

        model_as_dict = asdict(run_config)

        # Remove deprecated run_name
        model_as_dict.pop('run_name', None)

        # Remove deprecated platform
        model_as_dict.pop('platform', None)

        missing_fields = [field for field, value in model_as_dict.items() if value is None]
        if len(missing_fields) > 0:
            raise MCLIRunConfigValidationError(
                f'Cannot construct run because of missing field(s): {", ".join(missing_fields)}'
                '\nPlease pass the missing fields either through the yaml file or as command line arguments')
            # TODO: we could give the user what they should add to their yaml file directly

        # Fill in default initial values for FinalRunConfig
        model_as_dict.update({
            'run_id': uuid_generator(RUN_CONFIG_UID_LENGTH),
        })

        model_as_dict['name'] = _clean_run_name(model_as_dict['name'])

        if isinstance(model_as_dict.get('gpu_type'), int):
            model_as_dict['gpu_type'] = str(model_as_dict['gpu_type'])

        # Convert and validate optimization level
        try:
            model_as_dict['optimization_level'] = int(model_as_dict['optimization_level'])
            if model_as_dict['optimization_level'] not in VALID_OPTIMIZATION_LEVELS:
                raise ValueError
        except ValueError as e:
            raise MCLIRunConfigValidationError(
                f'"{model_as_dict["optimization_level"]}" is not a valid optimization level. '
                f'Please choose from: {", ".join(str(i) for i in VALID_OPTIMIZATION_LEVELS)}') from e

        if not validate_image(model_as_dict['image']):
            raise MCLIRunConfigValidationError(f'The image name "{model_as_dict["image"]}" is not valid')

        # Do not support specifying both a command and an entrypoint because the two might
        # conflict with each other
        if run_config.command and run_config.entrypoint:
            raise MCLIRunConfigValidationError('Specifying both a command and entrypoint as input is not supported.'
                                               'Please only specify one of command or entrypoint.')

        if not (run_config.command or run_config.entrypoint):
            raise MCLIRunConfigValidationError('Must specify one of command or entrypoint as input.')

        return cls(**model_as_dict)

    def to_create_run_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Convert a run configuration to a proper JSON to pass to MAPI's createRun

        Returns:
            Dict[str, Dict[str, Any]]: The run configuration as a MAPI runInput JSON
        """
        translations = {v: k for k, v in self._property_translations.items()}

        translated_input = {}
        for field_name, value in asdict(self).items():
            translated_name = translations.get(field_name, field_name)
            translated_input[translated_name] = value

        # Convert integrations to the nested format MAPI expects
        if 'integrations' in translated_input:
            integrations_list = []
            for integration in translated_input['integrations']:
                integration_type = integration['integration_type']

                # Get all entries except integration_type so we can nest them under params
                del integration['integration_type']

                translated_integration = {}
                for param, val in integration.items():
                    # Translate keys to camel case for MAPI parameters
                    translated_key = snake_case_to_camel_case(param)
                    translated_integration[translated_key] = val

                integrations_dict = {'type': integration_type, 'params': translated_integration}
                integrations_list.append(integrations_dict)
            translated_input['integrations'] = integrations_list

        return {
            'runInput': translated_input,
        }


def _clean_run_name(run_name: str) -> str:
    name_validation = validate_rfc1123_name(text=run_name)
    if name_validation.valid:
        return run_name

    # TODO: Figure out why logging strips out regex []
    # (This is a rich formatting thing. [] is used to style text)
    new_run_name = ensure_rfc1123_compatibility(run_name)

    logger.warning(f'Invalid run name "{run_name}": Run names must be less than 63 characters '
                   'and contain only lower-case letters, numbers, or "-". '
                   f'Converting to a valid name: {new_run_name}')
    return new_run_name


def _validate_cluster_exists(cluster: str):
    """Validate that the cluster exists, if not throw a MCLIValidationError
    """
    try:
        _ = MCLICluster.get_by_name(cluster)
    except KeyError as e:
        # pylint: disable-next=import-outside-toplevel
        from mcli.config import MCLIConfig

        conf = MCLIConfig.load_config(True)
        cluster_names = ', '.join([c.name for c in conf.clusters])
        if cluster_names:
            raise MCLIRunConfigValidationError(f'Invalid cluster requested: {cluster}. '
                                               'If you think this should be a valid cluster, try creating the cluster '
                                               f'first with:\n\nmcli create cluster {cluster}\n\n'
                                               f'Otherwise, choose one of: {cluster_names}') from e
        else:
            raise MCLIRunConfigValidationError(f'Invalid cluster requested: {cluster}. '
                                               'User has not created any clusters. '
                                               'If you think this should be a valid cluster, try creating the cluster '
                                               f'first with:\n\nmcli create cluster {cluster}') from e


@dataclass
class RunConfig:
    """A run configuration for the MosaicML Cloud

    Values in here are not yet validated and some required values may be missing.

    Args:
        name (`Optional[str]`): User-defined name of the run
        gpu_type (`Optional[str]`): GPU type (optional if only one gpu type for your cluster)
        gpu_num (`Optional[int]`): Number of GPUs
        cpus (`Optional[int]`): Number of CPUs
        cluster (`Optional[str]`): Cluster to use (optional if you only have one)
        image (`Optional[str]`): Docker image (e.g. `mosaicml/composer`)
        integrations (`List[Dict[str, Any]]`): List of integrations
        env_variables (`List[Dict[str, str]]`): List of environment variables
        command (`str`): Command to use when a run starts
        parameters (`Dict[str, Any]`): Parameters to mount into the environment
        entrypoint (`str`): Alternative to command
    """
    run_name: Optional[str] = None
    name: Optional[str] = None
    gpu_type: Optional[str] = None
    gpu_num: Optional[int] = None
    cpus: Optional[int] = None
    platform: Optional[str] = None
    cluster: Optional[str] = None
    image: Optional[str] = None
    optimization_level: Optional[int] = None
    integrations: List[Dict[str, Any]] = field(default_factory=list)
    env_variables: List[Dict[str, str]] = field(default_factory=list)

    command: str = ''
    parameters: Dict[str, Any] = field(default_factory=dict)
    entrypoint: str = ''

    def __post_init__(self):
        self.name = self.name or self.run_name
        if self.run_name is not None:
            logger.debug('Field "run_name" is deprecated. Please use "name" instead')

        self.cluster = self.cluster or self.platform
        if self.platform is not None:
            logger.debug('Field "platform" is deprecated. Please use "cluster" instead')

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def empty(cls) -> RunConfig:
        return cls()

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> RunConfig:
        """Load the config from the provided YAML file.

        Args:
            path (Union[str, Path]): Path to YAML file

        Returns:
            RunConfig: The RunConfig object specified in the YAML file
        """
        config = load_yaml(path)
        return cls.from_dict(config, show_unused_warning=True)

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = False) -> RunConfig:
        """Load the config from the provided dictionary.

        Args:
            dict_to_use (Dict[str, Any]): The dictionary to populate the RunConfig with

        Returns:
            RunConfig: The RunConfig object specified in the dictionary
        """
        field_names = list(map(lambda x: x.name, fields(cls)))

        unused_keys = []
        constructor = {}
        for key, value in dict_to_use.items():
            if key in field_names:
                constructor[key] = value

            else:
                unused_keys.append(key)

        if len(unused_keys) > 0 and show_unused_warning:
            warnings.warn(f'Encountered fields {unused_keys} which were not used in constructing the run.')

        return cls(**constructor)
