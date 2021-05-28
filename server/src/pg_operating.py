import os
import psycopg2
import sys

from src.config import PG_HOST, PG_PORT, PG_USER, PG_PASSWORD, PG_DATABASE, DEFAULT_TABLE


def connect_postgres_server():
    try:
        conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
        return conn
    except Exception as e:
        print("unable to connect to the database: ", e)
        sys.exit(2)


def create_pg_table(conn, cur):
    try:
        sql = "CREATE TABLE IF NOT EXISTS " + DEFAULT_TABLE + " (ids bigint, question text, answer text);"
        cur.execute(sql)
        conn.commit()
        print("create postgres table!")
    except Exception as e:
        print("can't create postgres table: ", e)
        sys.exit(2)


def create_question_table(conn, cur):
    try:
        sql = "CREATE TABLE IF NOT EXISTS question_data (question text, similarity text);"
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print("can't create postgres table question_data: ", e)
        sys.exit(2)


def insert_data(conn, cur, question, similarity_question):
    try:
        sql = "insert into question_data values ('" + question + "', '" + similarity_question + "');"
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print("faild insert data ", e)



def build_pg_index(conn, cur):
    try:
        sql = "CREATE INDEX IF NOT EXISTS " + DEFAULT_TABLE + "_index_ids on " + DEFAULT_TABLE + "(ids);"
        cur.execute(sql)
        conn.commit()
        print("build postgrs index sucessful!")
    except Exception as e:
        print("faild build index: ", e)


def copy_data_to_pg(f, conn, cur):
    try:
        cur.copy_from(f, DEFAULT_TABLE, sep='|')
        conn.commit()
        print("insert pg sucessful!")
    except Exception as e:
        print("copy data to postgres faild: ", e)
        sys.exit(2)


def search_in_pg(conn, cur, _id):
    # id_ = result[0].id
    sql = "select question, answer from " + DEFAULT_TABLE + " where ids = " + str(_id) + ";"
    #print(sql)
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        # print(rows)
        return rows
    except Exception as e:
        print("search faild: ", e)


def get_result_answer(conn, cur, question, table_name):
    sql = "select answer from " + table_name + " where question = '" + question + "';"
    # print(sql)
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        # print(rows)
        return rows
    except Exception as e:
        print("search faild: ", e)

