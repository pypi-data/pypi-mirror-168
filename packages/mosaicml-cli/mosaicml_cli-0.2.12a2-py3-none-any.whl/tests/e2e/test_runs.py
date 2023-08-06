"""Test everything end to end with a simple hello world yaml
"""
import datetime as dt
from concurrent.futures import TimeoutError
from copy import deepcopy
from time import sleep
from typing import Optional

import pytest
import pytz

from mcli.api import runs as runs_api
from mcli.api.exceptions import MAPIException
from mcli.api.model.run import Run
from mcli.models.run_config import RunConfig
from mcli.sdk import RunStatus
from tests.fixtures import HELLO_WORLD
from tests.mapi_config import mapi_config, set_mapi_config

RUN_DICT = deepcopy(HELLO_WORLD)
RUN_DICT['cluster'] = 'microk8s'

# TODO: HEK-1103
RUN_DICT['gpu_type'] = 'None'


def wait_for_run_status(run: Run, run_status: RunStatus, max_time: dt.datetime):
    """A naive implementation of kube wait_for_run_status to help with testing
    """
    while run.status < run_status and dt.datetime.now(tz=pytz.UTC) < max_time:
        sleep(5)
        if run.status == run_status or run.status in {RunStatus.FAILED, RunStatus.FAILED_PULL}:
            break

        runs = runs_api.get_runs([run])
        assert runs
        assert len(runs) == 1

        run = runs[0]

    assert run.status == run_status


@pytest.mark.e2e
class TestRunHelloWorld:
    """Tests all run endpoints using the hello world examples

    1. Starts one run as at setup
    2. Runs each test
    3. Deletes the run if needed during teardown
    """

    # Use non-finalized run config
    run_config = RunConfig.from_dict(RUN_DICT)

    created_run: Optional[Run] = None
    started_time: Optional[dt.datetime] = None
    max_time: Optional[dt.datetime] = None

    def setup_class(self):
        print('Creating a hello world job')

        now = dt.datetime.now(tz=pytz.UTC)
        self.started_time = now

        # This is a very simple job that should run locally in
        # under two minutes
        self.max_time = now + dt.timedelta(seconds=120)

        with set_mapi_config():
            self.created_run = runs_api.create_run(self.run_config)

    def teardown_class(self):
        print('Deleting any remaining hello world job artifact')

        if not self.created_run:
            return

        with set_mapi_config():
            try:
                runs_api.delete_runs([self.created_run])
            except MAPIException:
                # Should raise 404 if all tests pass (this is tested separately)
                pass

    @mapi_config
    def test_create_run_result(self):
        """Check just the run results that were created in setup

        All other create_run tests are done outside of this class
        """
        assert self.created_run and self.started_time and self.max_time
        assert self.created_run.name and self.run_config.name

        assert self.created_run.name.startswith(self.run_config.name)
        assert self.created_run.run_uid

        now = dt.datetime.now(tz=pytz.UTC)
        assert self.started_time < self.created_run.created_at < now < self.max_time
        assert self.started_time < self.created_run.updated_at < now < self.max_time

    @mapi_config
    def test_get_runs_by_name(self):
        """The run can be found by name or run object
        """
        assert self.created_run and self.started_time and self.max_time

        found_runs = runs_api.get_runs([self.created_run.name])
        assert found_runs
        assert len(found_runs) == 1

        found_runs = runs_api.get_runs([self.created_run])
        assert found_runs
        assert len(found_runs) == 1

    @mapi_config
    def test_get_runs_by_cluster(self):
        """The run can be found by cluster name
        """
        assert self.created_run and self.started_time and self.max_time
        assert self.run_config.cluster

        found_runs = runs_api.get_runs(
            runs=[self.created_run.name],
            clusters=[self.run_config.cluster],
        )
        assert found_runs
        assert len(found_runs) == 1

    @mapi_config
    def test_get_runs_all_filters(self):
        """The run can be found by specifying every single filter
        """
        assert self.created_run and self.started_time and self.max_time
        assert self.run_config.cluster

        assert self.run_config.gpu_type
        assert self.run_config.gpu_num
        found_runs = runs_api.get_runs(
            runs=[self.created_run.name],
            clusters=[self.run_config.cluster],
            gpu_types=[self.run_config.gpu_type],
            gpu_nums=[self.run_config.gpu_num],
        )
        assert found_runs
        assert len(found_runs) == 1

    @mapi_config
    def test_get_runs_unknown(self):
        """Getting an unknown run name returns 200
        """
        assert self.created_run and self.started_time and self.max_time

        found_runs = runs_api.get_runs(['unknown-run'])
        assert not found_runs

    @mapi_config
    def test_run_completes(self):
        """The run is marked as completed before the max time
        """
        assert self.created_run and self.started_time and self.max_time

        wait_for_run_status(self.created_run, RunStatus.COMPLETED, self.max_time)

        # The run can be found by completed status
        found_runs = runs_api.get_runs(
            [self.created_run.name],
            statuses=[RunStatus.COMPLETED],
        )
        assert found_runs
        assert len(found_runs) == 1

    @mapi_config
    @pytest.mark.skip
    def test_run_logs(self):
        """After the run has completed, run logs are available
        """
        raise NotImplementedError('TODO HEK-1168')

    @mapi_config
    def test_delete_runs(self):
        """The run is deleted
        """
        assert self.created_run and self.started_time and self.max_time

        # Delete a run
        deleted_runs = runs_api.delete_runs([self.created_run])
        assert deleted_runs
        assert len(deleted_runs) == 1

        deleted_run = deleted_runs[0]
        assert deleted_run.name == self.created_run.name

        # Check it is deleted
        found_runs = runs_api.get_runs([self.created_run])
        assert not found_runs

    @mapi_config
    def test_delete_runs_unknown(self):
        """Trying to delete an unknown run name returns a 404
        """
        with pytest.raises(MAPIException) as e:
            runs_api.delete_runs(['unknown-run'])


@mapi_config
@pytest.mark.e2e
def test_create_run_timeout(hello_world_run_config):
    run = RunConfig.from_dict(hello_world_run_config)
    with pytest.raises(TimeoutError):
        runs_api.create_run(run, timeout=0)


@mapi_config
@pytest.mark.e2e
def test_create_run_config_error(hello_world_run_config):
    run_config = deepcopy(hello_world_run_config)
    run_config['cluster'] = 'microk8s'
    run_config['image'] = None

    with pytest.raises(Exception):  # TODO: HEK-1191
        runs_api.create_run(RunConfig.from_dict(run_config))


@mapi_config
@pytest.mark.e2e
def test_create_run_command_error(hello_world_run_config):
    run_config = deepcopy(hello_world_run_config)
    run_config['cluster'] = 'microk8s'
    run_config['command'] = 'exit 1'

    # TODO: HEK-1103
    run_config['gpu_type'] = 'None'

    # Create a run that will error
    pending_run = runs_api.create_run(RunConfig.from_dict(run_config))
    assert pending_run

    # Run should throw an error
    max_time = dt.datetime.now(tz=pytz.UTC) + dt.timedelta(seconds=30)
    wait_for_run_status(pending_run, RunStatus.FAILED, max_time)


@mapi_config
@pytest.mark.e2e
def test_delete_run_timeout():
    with pytest.raises(TimeoutError):
        runs_api.delete_runs(['hi'], timeout=0)


@mapi_config
@pytest.mark.e2e
def test_get_run_timeout():
    with pytest.raises(TimeoutError):
        runs_api.get_runs(['hi'], timeout=0)
