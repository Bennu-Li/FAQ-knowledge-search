import os
from milvus import *

# MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_HOST = os.getenv("MILVUS_HOST", "192.168.1.85")
MILVUS_PORT = os.getenv("MILVUS_PORT", 19530)


PG_HOST = os.getenv("PG_HOST", "192.168.1.85")
# PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5432)
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_DATABASE = os.getenv("PG_DATABASE", "testdb")

DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "milvus_faq3")

collection_param = {
        'collection_name': DEFAULT_TABLE,
        'dimension': 768,
        'index_file_size': 1024,
        'metric_type': MetricType.IP
    }

