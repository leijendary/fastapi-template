from typing import List

from app.configs.app_config import app_config
from app.core.data.params import SortParams
from app.core.data.search_out import SearchOut
from fastapi_pagination import Params, create_page

_config = app_config()
language_default = _config.language_default

_match_all = {
    'match_all': {}
}


def translation_page(query, params: SortParams, fields):
    body = {
        'query': match_fuzziness(query, fields),
        **sorting(params.sort),
        **paginate(params.page, params.size)
    }

    return body


def to_page(result: dict, params: Params, type: SearchOut, locale=None):
    total = result['hits']['total']['value']
    locale = locale if locale else language_default
    records = [
        map_type(hit, type, locale)
        for hit in result['hits']['hits']
    ]

    return create_page(records, total, params)


def map_type(hit: dict, type: SearchOut, locale=None):
    return type({'id': hit['_id'], **hit['_source']}, locale)


def match_fuzziness(
    query='',
    fields: List[str] = [],
    fuzziness='AUTO',
    default=_match_all
):
    if not query:
        return default

    should = []

    for field in fields:
        match = {
            'match': {
                field: {
                    'query': query,
                    'fuzziness': fuzziness
                }
            }
        }

        should.append(match)

    return {
        'bool': {
            'should': should
        }
    }


def paginate(page, size):
    return {
        'from': (page - 1) * size,
        'size': size
    }


def sorting(sort: str):
    sort = sort if sort else '-_score'
    result = {}

    for s in sort.split(','):
        if s[0] not in ['+', '-']:
            # Default direction is asc
            s = '+' + s

        field = s[1:]
        direction = 'asc' if s[0] == '+' else 'desc'

        result[field] = direction

    return {
        'sort': result
    }
