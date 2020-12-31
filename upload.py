import json
import os
from elasticsearch import Elasticsearch, helpers, exceptions

client = Elasticsearch(os.getenv("ELASTICSEARCH_URL"))

f = open("dump", "r")


def main():
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        data = json.loads(line)
        yield {
            '_op_type': 'index',
            '_index': 'data',
            '_id': data["id"],
            'doc': data
        }


helpers.bulk(client, main(), stats_only=True, chunk_size=2000)
