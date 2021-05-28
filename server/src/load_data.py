from sentence_transformers import SentenceTransformer
from milvus import *
import pandas as pd
from sklearn.preprocessing import normalize
from io import StringIO

# from src.config import DEFAULT_TABLE
from src.milvus_operating import *
from src.pg_operating import *


def read_data(data_dir):
    print('read_data')
    data = pd.read_csv(data_dir)
    question_data = data['question'].tolist()
    answer_data = data['answer'].tolist()
    print(len(question_data))
    return question_data, answer_data


def get_embedding(question_data, model):
    print('get embedding')
    sentence_embeddings = model.encode(question_data)
    question_embeddings = normalize(sentence_embeddings)
    return question_embeddings




def get_postgres_data(ids, answer, question):
    f = StringIO()
    for i in range(len(ids)):
        line = str(ids[i]) + "|" + str(question[i]) + "|" + str(answer[i]) + "\n"
        f.write(line)
    f.seek(0)
    return f


def import_data(data_dir, client, conn, cursor):
    try:
        question_data, answer_data = read_data(data_dir)
    except Exception as e:
        print("read data faild: ", e)
        return False, "Failed to read data, please check the data file format."
    try:
        fname = 'temp.csv'
        create_collection(client)
        create_index(client)
        create_pg_table(conn, cursor)
        build_pg_index(conn, cursor)
        model = SentenceTransformer('paraphrase-mpnet-base-v2')
        question_embeddings = get_embedding(question_data, model)
        ids = insert_milvus(question_embeddings, client)
        # record_temp_csv(fname, ids, answer_data, question_data)
        f = get_postgres_data(ids, answer_data, question_data)
        copy_data_to_pg(f, conn, cursor)
        return True, "The data is loaded successfully."
    except Exception as e:
        print("load data faild: ", e)
        return False, "Failed to load data"


