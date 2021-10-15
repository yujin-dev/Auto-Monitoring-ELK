from elasticsearch import Elasticsearch, helpers
import json
import pandas as pd


class SEresult:

    def __init__(self, result):
        self.result = result

    def get_total(self):
        return self.result['hits']['total']['value']

    def get_hits(self):
        return pd.DataFrame(self.result['hits']['hits'])

    def get_source(self):
        _source = self.result['hits']['hits']
        return pd.DataFrame([res['_source'] for res in _source])


class SEutil:

    exclude_keys = ['took', 'timed_out', '_shards']

    def __init__(self, address):
        self.es = Elasticsearch(address)

    def organize(self, index, data: list):
        return [{"_index": index, "_source": res} for res in data]

    def insert_bulk(self, index, data:list):
        data = self.organize(index, data)
        helpers.bulk(self.es, data)

    def insert_data(self, index, data:dict):
        self.es.index(index=index, document=data)

    def get_query(self, index, query:dict, size=None):
        if size:
            query["size"] = size
        result = self.es.search(index=index, body=query)
        for key in self.exclude_keys:
            result.pop(key)
        return SEresult(result)

    def get_query_json(self, index, file, size=None):
        with open(file, "rb") as f:
            query = json.load(f)
        return self.get_query(index, query, size)

    def search_range(self, index, start_time, end_time):
        q = {
                "query": {
                    "range": {"timestamp":
                                {"gte":start_time, "lte": end_time}
                                }
                        }
            }
        return self.get_query(index, q)
