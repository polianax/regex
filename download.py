import json
import os
from elasticsearch import Elasticsearch, helpers, exceptions

client = Elasticsearch(os.getenv("ELASTICSEARCH_URL"))


def main():
    resp = helpers.scan(client, size=2000, index="data")

    for i, doc in enumerate(resp):
        data = doc["_source"].copy()
        data.pop("tags", None)
        yield data


fp = open("dump", 'w')
for item in main():
    jsonData = json.dumps(item)
    fp.write(jsonData + '\n')
