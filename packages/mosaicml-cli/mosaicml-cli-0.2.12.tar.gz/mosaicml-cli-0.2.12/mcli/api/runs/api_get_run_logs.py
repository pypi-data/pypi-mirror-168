"""Get a run's logs from the MosaicML Cloud"""
from __future__ import annotations

import textwrap
from concurrent.futures import Future
from typing import Any, Dict, Generator, Optional, Union, overload

import gql
from graphql import DocumentNode
from typing_extensions import Literal

from mcli.api.engine.engine import MAPIConnection
from mcli.api.model.run import Run
from mcli.utils.utils_kube import base64_decode


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> Generator[str, None, None]:
    ...


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[Generator[Future[str], None, None]]:
    ...


def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
) -> Union[Generator[str, None, None], Future[Generator[Future[str], None, None]]]:
    """Follow the logs for an active or completed run in the MosaicML Cloud

    This returns a :obj:`generator` of individual log lines, line-by-line, and will wait until
    new lines are produced if the run is still active.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with
            :func:`~mcli.sdk.get_runs`.
        rank (``Optional[int]``): Node rank of a run to get logs for. Defaults to the lowest
            available rank. This will usually be rank 0 unless something has gone wrong.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`follow_run_logs` will return immediately and the request will be
            processed in the background. The generator returned by the `~concurrent.futures.Future`
            will yield a `~concurrent.futures.Future` for each new log string returned from the cloud.
            This takes precedence over the ``timeout`` argument. To get the generator,
            use ``return_value.result()`` with an optional ``timeout`` argument and
            ``log_future.result()`` for each new log string.

    Returns:
        If future is False:
            A line-by-line :obj:`Generator` of the logs for a run
        Otherwise:
            A :class:`~concurrent.futures.Future` of a line-by-line generator of the logs for a run
    """

    # Convert to strings
    run_name = run.name if isinstance(run, Run) else run

    variables: Dict[str, Any] = {'runName': run_name}
    if rank is not None:
        variables['nodeRank'] = rank

    variable_data_name = 'getRunLogsInput'
    variables = {variable_data_name: variables}
    query = _build_query(variable_data_name)
    connection = MAPIConnection.get_current_connection()
    future_subscription = connection.pool.submit(_get_subscription_future, query, variables)

    if not future:
        subscription = future_subscription.result(timeout=timeout)
        return _get_resolved_generator(subscription)
    else:
        return future_subscription


def _build_query(variable_data_name: str) -> DocumentNode:
    """Build the GraphQL query
    """
    query_function = 'getRunLogs'
    query = textwrap.dedent(f"""
    subscription Subscription(${variable_data_name}: GetRunLogsInput!) {{
        {query_function}({variable_data_name}: ${variable_data_name})
    }}
    """)

    return gql.gql(query)


def _get_resolved_generator(log_generator: Generator[Future[str], None, None]) -> Generator[str, None, None]:
    """Automatically resolve the futures of a logs generator

    Args:
        subscription: A generator and yields futures for new values from a subscription

    Yields:
        Each new value from the subscription
    """
    for log_future in log_generator:
        # TODO: This does not handle keyboard interrupts nicely, requiring multiple presses.
        # On first glance, this isn't easy to fix.
        yield log_future.result()


def _get_subscription_future(query: DocumentNode, variables: Dict[str, Any]) -> Generator[Future[str], None, None]:
    """Get a future for the logs generator
    """
    connection = MAPIConnection.get_current_connection()
    subscription = connection.client.subscribe(query, variable_values=variables)

    def _get_logs_generator() -> Generator[Future[str], None, None]:
        try:
            while True:
                yield connection.pool.submit(_get_next_message, subscription)
        except StopIteration:
            return

    log_generator = _get_logs_generator()
    return log_generator


def _get_next_message(subscription: Generator[Dict[str, str], None, None]):
    """Get the next message from the GraphQL logging subscription
    """
    # TODO: This does not handle keyboard interrupts nicely, requiring multiple presses.
    # On first glance, this isn't easy to fix.
    data = next(subscription)

    # TODO: This will need to be hardened if MAPI might possibly send along chunks of logs
    # that might cut multi-byte characters. For now this should be fine
    message = base64_decode(data['getRunLogs'])
    return message
