import mysql.connector
from exceptions import *

class cwl:
    def __init__(self, host, user):
        self.host = host
        self.user = user

    def login(self, password):
        self.password = password
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()
        except:
            raise CWLLoginError

    def close(self):
        self.conn.close()

    def query(self, query, return_type=list):
        if return_type != dict:
            self.cursor.execute(query.replace("CANVAS", "TABLE").replace("COURSE", "COLUMN"))
            return [return_type(i) for i in self.cursor]
        else:
            dict_cursor = self.cursor(dictionary=True)
            return dict_cursor.execute(query.replace("CANVAS", "TABLE").replace("COURSE", "COLUMN"))

    def fetchall(self, return_type=list):
        if return_type != dict:
            return [return_type(i) for i in self.cursor.fetchall()]
        else:
            dict_cursor = self.cursor(dictionary=True)
            return dict_cursor.fetchall()

    def create_canvas(self, name, canvas_dict):
        table_str = ""
        for column in canvas_dict:
            table_str += f"{column['name']} {column['type']},\n"
        try:
            self.cursor.execute(f"CREATE TABLE {name} ({table_str})")
        except:
            raise CanvasCreationError