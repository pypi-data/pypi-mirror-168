"""get_secrets SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.schema.query import named_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.mcli_secret import Secret, get_secret_schema

__all__ = ['delete_secrets']


@overload
def delete_secrets(
    secrets: Optional[Union[List[str], List[Secret]]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[Secret]:
    ...


@overload
def delete_secrets(
    secrets: Optional[Union[List[str], List[Secret]]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[Secret]]:
    ...


def delete_secrets(
    secrets: Optional[Union[List[str], List[Secret]]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Deletes secrets from the MosaicML Cloud

    Arguments:
        secrets (:class:`~mcli.models.mcli_secret.Secret`): List of
            :class:`~mcli.models.mcli_secret.Secret` objects or secret name
            strings to delete.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`delete_secrets` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.mcli_secret.Secret` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    # Convert to strings
    secret_names = []
    if secrets:
        secret_names = [s.name if isinstance(s, Secret) else s for s in secrets]

    filters = {}
    if secret_names:
        filters['name'] = {'in': secret_names}

    query_function = 'deleteSecrets'
    variable_data_name = 'getSecretsData'
    variables = {
        variable_data_name: {
            'filters': filters,
        },
    }

    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName=variable_data_name,
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.GET_SECRETS_INPUT,
    )

    query = named_query(
        query_name='DeleteSecrets',
        query_function=query_function,
        query_items=get_secret_schema(),
        variables=[graphql_variable],
        is_mutation=True,
    )

    response = run_plural_mapi_request(
        query=query,
        query_function=query_function,
        return_model_type=Secret,
        variables=variables,
    )

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
