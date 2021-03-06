import os
import re
from elasticsearch import Elasticsearch, helpers, exceptions

client = Elasticsearch(os.getenv("ELASTICSEARCH_URL"))

positive = re.compile(r'[\W](?:proced(?:ente|ência|eu|er))|(inadmissibilidade|inadmit(?:o|indo) (?:liminarmente)(?:d\w|o) recurso)',
                      re.IGNORECASE)

inverse = re.compile(r'neg(?:ar|o|ando)(?:-lhes?)? provimento', re.IGNORECASE)

ignore = re.compile(r'[dn]a lide'
                    r'|-{89}|_{89}'
                    r'|PAGE \\#'
                    r'|[\W]solidário'
                    r'|julgador\s*$', re.IGNORECASE)

negative = re.compile(r'[\W](?:improced(?:ente|ência|eu|er))'
                      r'|pela nulidade'
                      r'|anul(ar|o|ando)'
                      r'|(?:acat(?:o|ando|ar)|acolh(?:o|er|endo|imento))(?: d?a)? preliminar d\w nul'
                      r'|(?:julg|declar|consider)(?:o|ando|ou|ar)( parcialmente)? nul[oa]'
                      r'|nul(o|idade) .?ab initio', re.IGNORECASE)

returnRe = re.compile(r'autos retornarem'
                      r'|retornar .*(?:camer|câmara|instância|cjul|gepre|nupre|[àa] fase|pge|[aà]o? julgad|ao órgão)',
                      re.IGNORECASE)


def read(sent):
    result = {
        "negative": False,
        "positive": False,
        "undefined": False,
        "ignored": False,
        "return": False
    }
    # Se deve retornar, não deve considerar o julgamento
    if returnRe.search(sent):
        result["return"] = True
    else:
        if negative.search(sent):
            result["negative"] = True
        if positive.search(sent):
            result["positive"] = True
        if (not (result["positive"] or result["negative"])) and ignore.search(sent):
            result["ignored"] = True
        if not (result["positive"] or result["negative"] or result["ignored"]):
            result["undefined"] = True
    return result


def tag(item):
    result = read(item["lastSentence"])
    if result["undefined"]:
        result = read(item["penultimateSentence"])
    item["tags"] = result


def main():
    resp = helpers.scan(client, size=2000, index="data")

    for i, doc in enumerate(resp):
        data = doc["_source"].copy()
        tag(data)
        yield {
            '_op_type': 'update',
            '_index': 'data',
            '_id': doc["_id"],
            'doc': data
        }


helpers.bulk(client, main(), stats_only=True, chunk_size=2000)
