from milvus import *
from sklearn.preprocessing import normalize

from src.milvus_operating import *
from src.pg_operating import *


def get_similar_questions(results, conn, cursor):
    out_put = []
    for result in results[0]:
        rows = search_in_pg(conn, cursor, result.id)
        if rows and len(rows[0]) > 0:
            out_put.append(rows[0])
    return out_put


def record_question(conn, cursor, question, similarity_question):
    create_question_table(conn, cursor)
    insert_data(conn, cur, question, similarity_question)


def search_data(question, client, conn, cursor, model):
    embed = model.encode(question)
    embed = embed.reshape(1, -1)
    embed = normalize(embed)
    query_embeddings = embed.tolist()
    status, results = milvus_search(client, query_embeddings)
    out_put = get_similar_questions(results, conn, cursor)
    record_question(conn, cursor, question, out_put[0][0])
    # print(out_put)
    return out_put



