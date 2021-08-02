"""request related middlewares."""

import functools
import json
import uuid
from typing import Any, AnyStr, Callable, Dict, Type

from src.commons import context, http, utils
from src.commons.logging import logger
from src.commons.types import CaseInsensitiveMapping


def validate(schema: Dict[AnyStr, Any] = None, bind_type: Type = None) -> Callable:
    """Validates request schema and binds body to a specific object type.

    :param schema: JSON schema definition
    :param bind_type: Object model type
    """

    def inner(func: Callable) -> Callable:
        """Middleware function."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """Middleware logic."""

            event, _ = args

            body = {}
            headers = CaseInsensitiveMapping(event['headers'])
            trace_id = str(uuid.uuid4())

            if headers.get('Trace-Id', None) is not None:
                trace_id = headers.get('Trace-Id')

            logger.context.field('trace_id', trace_id)
            context.set_value('trace_id', trace_id)

            request_data = {
                'headers': headers,
                'path_params': event['pathParameters'] if event['pathParameters'] is not None else {},
                'query_params': event['queryStringParameters'] if event['queryStringParameters'] is not None else {},
                'path': event['requestContext']['path'],
                'method': event['requestContext']['httpMethod'],
            }

            if event['body']:
                body = json.loads(event['body'])

            request_data['body'] = body
            context.set_value('request', request_data)

            if schema is not None:
                try:
                    body = utils.validate_json_schema(body, schema)
                except Exception as err:
                    return http.json_error(err)

            if bind_type is not None and 'from_dict' in dir(bind_type):
                body = bind_type.from_dict(body)

            request_data['body'] = body
            context.set_value('request', request_data)

            return func(*args, **kwargs)

        return wrapper

    return inner
