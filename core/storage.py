"""Small local SQLite store for durable material-recognition history."""
import sqlite3
from pathlib import Path
DB=Path(__file__).resolve().parents[1]/'data'/'app_history.sqlite3'
def connect():
    DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB); c.execute('CREATE TABLE IF NOT EXISTS recognition_history (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, material TEXT NOT NULL, confidence REAL NOT NULL, model TEXT NOT NULL, filename TEXT)'); c.commit(); return c
def add_recognition(created_at, material, confidence, model, filename=''):
    with connect() as c: c.execute('INSERT INTO recognition_history(created_at,material,confidence,model,filename) VALUES(?,?,?,?,?)',(created_at,material,float(confidence),model,filename))
def get_recognition_history(limit=100):
    with connect() as c: rows=c.execute('SELECT created_at,material,confidence,model,filename FROM recognition_history ORDER BY id DESC LIMIT ?', (int(limit),)).fetchall()
    return [{'time':r[0],'class':r[1],'confidence':r[2],'model':r[3],'filename':r[4]} for r in rows]
def clear_recognition_history():
    with connect() as c: c.execute('DELETE FROM recognition_history')
