# utils/es.py
from elasticsearch import Elasticsearch

ES_HOST = "http://localhost:9200"
ES_INDEX = "assets"

es = Elasticsearch(ES_HOST)

