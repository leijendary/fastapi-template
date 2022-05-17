from typing import Type

from fastapi_pagination import Params, create_page

from app.core.context.request_context import current_language
from app.core.data.params import SortParams
from app.core.data.search_out import SearchOut

MATCH_ALL = {
    "match_all": {}
}


def translation_page(query, params: SortParams, fields):
    body = {
        "query": match_fuzziness(query, fields),
        **sorting(params.sort),
        **paginate(params.page, params.size)
    }

    return body


def to_page(result: dict, params: Params, to_type: Type[SearchOut]):
    total = result["hits"]["total"]["value"]
    records = [map_type(hit, to_type) for hit in result["hits"]["hits"]]

    return create_page(records, total, params)


def map_type(hit: dict, to_type: Type[SearchOut]):
    locale = current_language()

    return to_type(locale=locale, id=hit["_id"], **hit["_source"])


def match_fuzziness(query="", fields=None, fuzziness="AUTO", default=None):
    if fields is None:
        fields = []

    if default is None:
        default = MATCH_ALL

    if not query:
        return default

    should = []

    for field in fields:
        match = {
            "match": {
                field: {
                    "query": query,
                    "fuzziness": fuzziness
                }
            }
        }

        should.append(match)

    return {
        "bool": {
            "should": should
        }
    }


def paginate(page, size):
    return {
        "from": (page - 1) * size,
        "size": size
    }


def sorting(sort: str):
    sort = sort if sort else "-_score"
    result = {}

    for s in sort.split(","):
        if s[0] not in ["+", "-"]:
            # Default direction is asc
            s = "+" + s

        field = s[1:]
        direction = "asc" if s[0] == "+" else "desc"

        result[field] = direction

    return {
        "sort": result
    }
