from typing import List

from app.configs.app_config import app_config
from app.core.data.search_out import SearchOut
from fastapi_pagination import Page, Params, create_page

config = app_config()
language_default = config.language_default

_match_all = {
    'match_all': {}
}


def translation_page(query, fields, page, size, sort):
    body = {
        'query': match_fuzziness(query, fields),
        **sorting(sort),
        **paginate(page, size)
    }

    return body


def to_page(result: dict, page, size, type: SearchOut, locale=None) -> Page:
    total = result['hits']['total']['value']
    records = [
        type({'id': hit['_id'], **hit['_source']}, locale)
        for hit in result['hits']['hits']
    ]

    return create_page(records, total, Params(page=page, size=size))


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


def paginate(page: int, size: int):
    page = int(page) if page else 1
    size = int(size) if size else 10

    return {
        'from': (page - 1) * size,
        'size': size
    }


def sorting(sort: List[str]):
    sort = sort if sort else ['_score,desc']
    result = {}

    for s in sort:
        params = s.split(',')
        field = params[0]
        value = params[1] if len(params) == 2 else 'asc'

        result[field] = value

    return {
        'sort': result
    }
