NGRAM_ANALYZER = {
    "index": {
        "max_ngram_diff": 20
    },
    "analysis": {
        "analyzer": {
            "ngram_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "ngram_filter"
                ]
            }
        },
        "filter": {
            "ngram_filter": {
                "type": "ngram",
                "min_gram": 2,
                "max_gram": 20
            }
        }
    }
}
