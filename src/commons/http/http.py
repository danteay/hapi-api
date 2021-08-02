"""Http common functions."""

import decimal
import http.client
import json as json_parser
import os
from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Tuple, Union

from src.commons import context
from src.commons.errors import HandlerError
from src.commons.logging import logger


def json(
    code: Optional[int] = 200,
    body: Optional[Dict[AnyStr, Any]] = None,
    error: Optional[Any] = None,
    headers: Optional[Dict[AnyStr, AnyStr]] = None,
) -> Dict[AnyStr, Any]:
    """Http JSON lambda response.
    :param code: Http response code
    :param body: Response json body
    :param error: Possible error on response body
    :param headers: Response headers
    :return Dict: Response payload
    """

    if not body:
        body = {}

    if not headers:
        headers = {}

    _log_request_data(_mask_protected_data(body))

    body = _validate_error(body, code, error)
    body = json_parser.dumps(body, default=_handle_extra_types)

    return response(code=code, body=body, headers=headers)


def json_error(error: Any, headers: Optional[Dict[AnyStr, AnyStr]] = None) -> Dict[AnyStr, Any]:
    """Respond with an standard XML error description.
    :param error: Possible error to handle
    :param headers: Add extra response headers
    :return Dict: Response payload
    """

    if not headers:
        headers = {}

    if isinstance(error, HandlerError):
        return json(code=error.code, error=error, headers=headers)

    return json(code=500, error=error, headers=headers)


def response(
    code: Optional[int] = 200,
    body: Optional[AnyStr] = None,
    headers: Optional[Dict[AnyStr, AnyStr]] = None,
) -> Dict[AnyStr, Any]:
    """Http lambda response formatting.
    :param code: Http response code
    :param body: Response json body
    :param headers: Response headers
    :return: Response
    """

    if not headers:
        headers = {}

    if os.getenv('CORS', 'false') == 'true':
        headers.update(_cors_headers())

    return {
        'statusCode': code,
        'body': body,
        'headers': headers,
    }


def csv(
    code: Optional[int] = 200,
    body: Optional[AnyStr] = None,
    headers: Optional[Dict[AnyStr, AnyStr]] = None,
    file_name: Optional[AnyStr] = 'file',
) -> Dict[AnyStr, Any]:
    """Http lambda response file formatting.
    :param code: Http response code
    :param body: Response body
    :param headers: Response headers
    :param file_name: Name for the csv file
    :return: Response
    """

    if not headers:
        headers = {}

    headers['Content-type'] = 'text/csv; charset="UTF-8"'
    headers['Content-Disposition'] = 'attachment; filename={0}.csv'.format(file_name)

    return response(code=code, body=body, headers=headers)


def _log_request_data(body: Any) -> NoReturn:
    """Add base request data to logger.

    :param body: Response body
    """

    logger.fields(
        {
            'path': context.get_value('request').get('path'),
            'method': context.get_value('request').get('method'),
            'request': _get_request(),
            'response': body,
        },
    )


def _validate_error(body: Dict[AnyStr, Any], code: int, error: Any) -> Dict[AnyStr, Any]:
    """From current response validate and generate error response.

    :param code: Http response code
    :param body: Response json body
    :param error: Possible error on response body
    :return Dict[AnyStr, Any]: Response body
    """

    if error is not None:
        error_code, error_message, root_causes = _process_error(code, error)
        body['error'] = error_code
        body['message'] = error_message
        body['root_causes'] = root_causes

    if 'error' in body and body['error'] is not None:
        logger.error('handled request', error=body['error'])
    else:
        logger.info('handled request')

    return body


def _get_error_from_code(code: int) -> AnyStr:
    """Transform http status code into a standard error message.
    :param code: HTTP status code
    :return AnyStr: Associated status code message
    """

    error = http.client.responses[code]
    error = error.lower().replace(' ', '-')
    return error


def _cors_headers() -> Dict[AnyStr, AnyStr]:
    """Add cors headers to response headers.
    :return Dict: Default value of Cors headers
    """

    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'POST,GET,OPTIONS,PUT,DELETE',
        'Access-Control-Allow-Headers': 'x-user-id',
    }


def _process_error(code: int, error: Any) -> Tuple[int, AnyStr, List]:
    """Get proper messages from errors according his type.

    :param code: Current status code of the handled error
    :param error: Error to be handled
    :return: tuple of error code and error message
    """

    if isinstance(error, HandlerError):
        code = error.message
        message = error.description
        root_causes = error.root_causes
    else:
        code = _get_error_from_code(code)
        message = 'Unexpected error'
        root_causes = [{'message': str(error).replace('\n', '')}]

    return code, message, root_causes


def _handle_extra_types(obj: Any) -> Any:
    """Default Json serializer for types that can be handled itself.

    :param obj: Object data to serialize
    :return: Serialized value
    """

    # Lambda will automatically serialize decimals so we need
    # to support that as well.
    if isinstance(obj, decimal.Decimal):
        return float(obj)

    try:
        return str(obj)
    except Exception as err:
        message = f'Object of type {obj.__class__.__name__} is not JSON serializable'
        raise TypeError(message) from err


def _get_request() -> Dict[AnyStr, Any]:
    """Get proper formatted request body.
    :return Dict: Request body on dict format
    """

    body = context.get_value('request').get('body')

    if isinstance(body, dict):
        return _mask_protected_data(body)

    if 'to_dict' in dir(body):
        return _mask_protected_data(body.to_dict())

    return body


def _mask_protected_data(data: Union[Dict[AnyStr, Any], List[Any]]) -> Dict[AnyStr, Any]:
    """Mask values of protected data for logging.

    :param data: Data to mask protected params
    :return Dict[AnyStr, Any]: Masked data
    """

    if isinstance(data, list):
        data = _mask_list_data(data)

    if isinstance(data, dict):
        data = _mask_dict_data(data)

    return data


def _mask_list_data(data: List[Any]) -> List[Any]:
    """Mask list data."""

    for index, value in enumerate(data):
        data[index] = _mask_protected_data(value)

    return data


def _mask_dict_data(data: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
    """Mask dict data."""

    protected = {
        'password',
        'password_confirmation',
    }

    for key in data.keys():
        if key in protected:
            data[key] = '******'
            continue

        data[key] = _mask_protected_data(data[key])

    return data
