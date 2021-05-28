from milvus import *
import time
import sys
from src.config import DEFAULT_TABLE as TABLE_NAME
from src.config import MILVUS_HOST, MILVUS_PORT, DEFAULT_TABLE


def milvus_client():
    try:
        client = Milvus(host=MILVUS_HOST, port=MILVUS_PORT)
        return client
    except Exception as e:
        print("Milvus client error:", e)


def create_collection(client):
    collection_param = {
        'collection_name': DEFAULT_TABLE,
        'dimension': 768,
        'index_file_size': 1024,
        'metric_type': MetricType.IP
    }
    if not client.has_collection(DEFAULT_TABLE)[1]:
        status = client.create_collection(collection_param)
        print(status)


def drop_milvus_table(table_name, client):
    try:
        status = client.drop_collection(table_name)
    except Exception as e:
        print("Milvus drop table error:", e)


def create_index(client):
    param = {'nlist': 500}
    try:
        status = client.create_index(DEFAULT_TABLE, IndexType.IVF_FLAT, param)
        print(status)
    except Exception as e:
        print("Milvus create index error:", e)



def insert_milvus(question_embeddings, client):
    try:
        status, ids = client.insert(collection_name=DEFAULT_TABLE, records=question_embeddings)
        print(status)
        return ids
    except Exception as e:
        print("Milvus insert error:", e)



def milvus_search(client, vec):
    try:
        SEARCH_PARAM = {'nprobe': 40}
        status, results = client.search(collection_name=DEFAULT_TABLE, query_records=vec, top_k=10, params=SEARCH_PARAM)
        return status, results
    except Exception as e:
        print("Milvus search error:", e)


def get_milvus_rows(client, table_name):
    try:
        status, results = client.count_entities(collection_name=table_name)
        return results
    except Exception as e:
        print("get milvus entity rows error: ", e)
        sys.exit(2)
