import logging

from flask_cors import CORS
from flask import Flask, request, send_file, jsonify
from flask_restful import reqparse

from src.const import UPLOAD_PATH

from sentence_transformers import SentenceTransformer

from src.milvus_operating import milvus_client
from src.pg_operating import connect_postgres_server
from src.get_answer import search_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['JSON_SORT_KEYS'] = False
CORS(app)

client = milvus_client()
model = SentenceTransformer('paraphrase-mpnet-base-v2')


@app.route('/api/v1/search', methods=['POST'])
def do_search_api():
    global conn
    args = reqparse.RequestParser(). \
        add_argument("Table", type=str). \
        add_argument("query_text", type=str). \
        parse_args()

    question = args['query_text']
    if not question:
        return "no question"
    if question:
        try:
            conn = connect_postgres_server()
            cursor = conn.cursor()
            output = search_data(question, client, conn, cursor, model)
            if output:
                result = {"response": output}
                return result
            else:
                return "There is no data"
        except Exception as e:
            return "Error with {}".format(e)
        finally:
            conn.close()
    return "not found", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0")
