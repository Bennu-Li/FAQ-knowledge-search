
from sentence_transformers import SentenceTransformer

from src.load_data import import_data
from src.milvus_operating import milvus_client
from src.pg_operating import connect_postgres_server
from src.get_answer import search_data



def insert_data(data_dir):
    client = milvus_client()
    conn = connect_postgres_server()
    cursor = conn.cursor()
    import_data(data_dir, client, conn, cursor)


def get_results(question):
    client = milvus_client()
    conn = connect_postgres_server()
    cursor = conn.cursor()
    model = SentenceTransformer('paraphrase-mpnet-base-v2')
    out_put = search_data(question, client, conn, cursor, model)
    return out_put


insert_data('Cleaned_Data.csv')
insert_data('issue-qa.csv')
insert_data('dicussion-qa.csv')
res = get_results('How to set index_file_size')
print(res)
