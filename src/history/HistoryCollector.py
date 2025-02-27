import sqlite3


def create_history_base():
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INT auto_increment primary key, id_tg varchar(50), topic varchar(50), mark INT)')
    conn.commit()
    cur.close()
    conn.close()


def add_history(id_tg, topic, mark):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (id_tg, topic, mark) VALUES ("%s", "%s", "%s")' % (id_tg, topic, mark))
    conn.commit()
    cur.close()
    conn.close()

