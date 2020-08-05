from flask import g
import sqlite3

path_to_db = "/home/seraphina/Documents/PROJECTS/PROJECTS_2020/TALENTBLENDER/TALENTBLENDER_MVP_1"

def connect_db():
    sql = sqlite3.connect(path_to_db + "/members.db")
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db