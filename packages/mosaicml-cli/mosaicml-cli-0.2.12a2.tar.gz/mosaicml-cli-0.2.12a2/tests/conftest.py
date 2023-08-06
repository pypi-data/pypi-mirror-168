""" Conftest for Fixtures """
# Copyright 2021 MosaicML. All Rights Reserved.

import os
import pathlib
from typing import List

import pytest

from mcli import config

# Add the path of any pytest fixture files you want to make global
pytest_plugins = ['tests.fixtures', 'tests.cli.fixtures', 'tests.api.fixtures']


@pytest.fixture(scope='session', autouse=True)
def tests_setup_and_teardown():
    # Will be executed before the first test
    old_environ = dict(os.environ)
    for env_var in (config.MCLI_MODE_ENV,):
        os.environ.pop(env_var, default=None)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption('--e2e',
                     action='store_true',
                     help="""\
        Use this flag to run end-to-end test on the MosaicML Cloud
        Make sure that you have a valid API key either in the
        mcli_config or set as an environment variable, and all
        services are running locally before running these tests.""")
    parser.addoption('--integration',
                     action='store_true',
                     help="""\
        Use this flag to run integration tests. These tests take longer to run
        than unit tests, but can use microk8s to submit actual manifests to a real
        Kubernetes cluster. You will need to install microk8s.""")


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]) -> None:
    deselected = set()

    # We only run api tests exclusively
    e2e = bool(config.getoption('e2e'))
    for item in items:
        if e2e ^ (item.get_closest_marker('e2e') is not None):
            deselected.add(item)

    # We only run integration tests exclusively, and only if pytest is invoked accordingly
    integration = bool(config.getoption('integration'))
    integration_dir = config.rootpath / 'tests/integration'
    for item in items:
        if integration ^ (integration_dir in pathlib.Path(item.fspath).parents):
            deselected.add(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = [i for i in items if i not in deselected]
