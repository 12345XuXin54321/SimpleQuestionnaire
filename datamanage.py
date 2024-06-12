import sqlite3
import os

DB_NAME = "data.db"


def init_dbfile(db_file_path):
    db_conn = sqlite3.connect(db_file_path)
    db_conn.text_factory = bytes
    cur = db_conn.cursor()

    sql = "create table question_tab (ind INT, content TEXT);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table questionnaire_tab (ind INT, title VARCHAR);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table respondents_tab (ind INT);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table answer_tab (ind INT, content TEXT);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table users_tab (user_ind INT, username VARCHAR);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table questionnaire_data_tab (ques_ind INT, naire_ind INT, ind INT);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table create_questionnaire_tab (user_ind INT, naire_ind INT);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table reply_questionnaire_tab (user_ind INT, respondents_ind INT);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table respondents_data_tab (respondents_ind INT, answer_ind INT, ind INT);"
    cur.execute(sql)
    db_conn.commit()

    sql = "create table questionnaire_fillout_tab (respondents_ind INT, naire_ind INT);"
    cur.execute(sql)
    db_conn.commit()

    cur.close()
    db_conn.close()


class DataManage():
    def __init__(self) -> None:
        os.system("rm data.db")
        if (not os.path.isfile(DB_NAME)):
            init_dbfile(DB_NAME)
        self.db_connent = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.db_cursor = self.db_connent.cursor()

    def execute_sql(self, sql):
        print(sql)
        db_data = self.db_cursor.execute(sql)
        self.db_connent.commit()
        db_data = list(db_data)
        print(db_data)
        return db_data

    def get_data(self, tab_name, select_data, condition=None):
        sql = "select " + select_data + " from " + tab_name
        if condition != None:
            sql = sql + " where " + condition
        sql = sql + ";"
        return self.execute_sql(sql)

    def insert_data(self, tab_name, db_data: list):
        data_sql = str(db_data)
        data_sql = data_sql[1:-1]
        data_sql = "(" + data_sql + ")"

        sql = "insert into " + tab_name + " values" + data_sql + ";"

        self.execute_sql(sql)

    def db_len(self, tab_name):
        t_count = self.get_data(tab_name, "count(*)", "1=1")
        t_count = list(t_count[0])
        t_count = t_count[0]
        return t_count


a = DataManage()
