
import sqlite3
from flask import g

def getConnection():
    connection= sqlite3.connect("clinidata.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory= sqlite3.Row
    return connection

def execute(sql, params=[]):
    connection= getConnection()
    result= connection.execute(sql, params)
    connection.commit()
    g.lastInsertId= result.lastrowid
    connection.close()

def lastInsertId():
    return g.lastInsertId    
    
def query(sql, params=[]):
    connection= getConnection()
    result= connection.execute(sql, params).fetchall()
    connection.close()
    return result