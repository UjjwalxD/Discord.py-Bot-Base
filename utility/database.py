import sqlite3
from utility.logger import logger

def database():
    conn = sqlite3.connect('core/database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (username text, password text)""")
    conn.commit()
    logger("[DATABASE] Connected to 'core/database.db'", "yellow")