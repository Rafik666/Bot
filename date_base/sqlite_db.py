import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('profiles_players')
    cur = base.cursor()
    if base:
        print('Data base connect OK!')
    base.execute('CREATE TABLE IF NOT EXISTS players(users TEXT, id INTEGER PRIMARY KEY, money INTEGER, win INTEGER, lost INTEGER, max_win INTEGER, max_bit INTEGER)')
    base.commit()

async def sql_add_command(state):
    
    cur.execute('INSERT INTO players VALUES (?,?,?,?,?,?,?)', state)
    base.commit()


