"""Common utilities."""

import os
from base64 import urlsafe_b64encode
from typing import Any, AnyStr, Dict, NoReturn, Tuple

import fastjsonschema
import requests

from src.commons import context
from src.commons.errors import HandlerError, SchemaError
from src.commons.logging import logger


def short_id(length: int = 6) -> AnyStr:
    """Generate and return a short ID of N chars between 6 and 50.
    :param length: total of characters of the short_id
    :return AnyStr: Short ID string
    """

    length = max(length, 6)
    length = min(length, 50)

    rand = urlsafe_b64encode(os.urandom(100)).decode('utf-8').upper()
    rand = rand.replace('-', '').replace('_', '').replace('=', '')
    return rand[0:length]


def validate_json_schema(data: Dict[AnyStr, Any], schema: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
    """Validate JSON request payload with a given JSON schema.
    :param data: JSON request data
    :param schema: JSON schema definition
    :return Dict: Evaluated data
    :raise SchemaError: On validation error
    """

    try:
        validate = fastjsonschema.compile(schema)
        return validate(data)
    except Exception as err:
        raise SchemaError(err) from err


def call_service(
    method: AnyStr,
    resource: AnyStr,
    headers: Dict[AnyStr, AnyStr] = None,
    json: Dict[AnyStr, Any] = None,
    params: Dict[AnyStr, Any] = None,
    service_name: AnyStr = None,
) -> Tuple[int, Dict[AnyStr, Any]]:
    """Generic async call to an HTTP resource.
    :param method: Request method GET, POST, PUT or DELETE
    :param resource: Resource service endpoint
    :param headers: Request headers
    :param json: JSON body for the request
    :param params: URL params data on the request
    :param service_name: Name of the service that will be called
    :return Tuple: Status code and json response
    :raise HandlerError: On status code is not 200, 201 or 202
    """

    options = _build_request_options(method, resource, headers, json, params)

    logger.field('service', service_name).fields(options, ).debug('calling service')

    res = _execute_request(method, options)

    try:
        json_res = res.json()
    except Exception as err:
        logger.error('not json response', err)
        raise HandlerError(
            code=500,
            message='response-parse-error',
            description="Can't parse as json the external response call",
            root_causes=[{
                'status_code': res.status_code,
                'response': res.text,
            }],
        ) from err

    if res.status_code in {200, 201, 202}:
        return res.status_code, json_res

    raise _raise_call_service_exception(
        code=res.status_code,
        response=json_res,
        service_name=service_name,
    )


def _raise_call_service_exception(code: int, response: Dict[AnyStr, Any], service_name: AnyStr) -> NoReturn:
    """Raise and exception according response and code.
    :param code: Status code of the call request
    :param response: Response payload obtained from the call
    :raise HandlerError: Configured handler error
    """

    logger.fields({
        'service_name': service_name,
        'status_code': code,
        'service_response': response,
    }, ).error('service call error')

    res_keys = response.keys()

    message = 'service-call-error'
    description = 'Error calling external service'
    root_causes = []

    if 'root_causes' in res_keys:
        root_causes = response['root_causes']

    if 'description' in res_keys:
        description = response['description']

    if 'message' in res_keys:
        message = response['message']

    root_causes.append({'message': f'Error calling service {service_name}'})

    return HandlerError(
        code=code,
        message=message,
        description=description,
        root_causes=root_causes,
    )


def _build_request_options(
    method: AnyStr,
    resource: AnyStr,
    headers: Dict[AnyStr, AnyStr] = None,
    json: Dict[AnyStr, Any] = None,
    params: Dict[AnyStr, Any] = None,
) -> Dict[AnyStr, Any]:
    """Validate configs and build request options.
    :param method: Request method GET, POST, PUT or DELETE
    :param resource: Resource service endpoint
    :param headers: Request headers
    :param json: JSON body for the request
    :param params: URL params data on the request
    :return Dict: Request configuration
    :raise requests.exceptions.RequestException: On configured invalid request method
    """

    _validate_request_method(method)

    if not headers:
        headers = {}

    headers.update({'Trace-Id': context.get_value('trace_id')})

    options = {
        'url': resource,
        'headers': headers,
    }

    options = _add_request_data(method, options, json, params)
    return options


def _validate_request_method(method: AnyStr) -> NoReturn:
    """Validate if the specified request method is valid.
    :param method: Method name
    :raises requests.exceptions.RequestException: For unsupported request method
    """

    method = method.upper()

    if method not in {'GET', 'POST', 'PUT', 'DELETE'}:
        raise requests.exceptions.RequestException('invalid request method')


def _add_request_data(
    method: AnyStr,
    options: Dict[AnyStr, Any],
    json: Dict[AnyStr, Any] = None,
    params: Dict[AnyStr, Any] = None,
) -> Dict[AnyStr, Any]:
    """Add request data to teh request call options.
    :param method: Request method
    :param options: Options to be updated
    :param json: Json data
    :param params: Query params data
    :return Dict[AnyStr, Any]: Updated request options
    """

    if json is not None and method in {'POST', 'PUT', 'DELETE'}:
        options['json'] = json

    if params is not None and method == 'GET':
        options['params'] = params

    return options


def _execute_request(method: AnyStr, options: Dict[AnyStr, Any]) -> requests.Response:
    """Execute requests library call to any REST service configured.
    :param method: HTTP request method to execute call
    :param options: Configured options for the call
    :return requests.Response: Response call
    :raise requests.exceptions.RequestException: On configured invalid request method
    """

    method = method.upper()

    if method == 'GET':
        return requests.get(**options)

    if method == 'POST':
        return requests.post(**options)

    if method == 'PUT':
        return requests.put(**options)

    if method == 'DELETE':
        return requests.delete(**options)

    raise requests.exceptions.RequestException('invalid request method')
