import sqlite3
import wave

BASE = 'base.sqlite'


def get_logins_from_user():
    bd = sqlite3.connect(BASE)
    cur = bd.cursor()
    logins = [i[0] for i in cur.execute("""SELECT login FROM user""").fetchall()]
    bd.close()
    return logins


def register_user(login: str, password: str):
    if login not in get_logins_from_user():
        data = (str(login), str(password))
        bd = sqlite3.connect(BASE)
        cur = bd.cursor()
        cur.execute("""INSERT INTO user(login, password) VALUES(?, ?)""", data)
        bd.commit()
        bd.close()
    else:
        return 1


def check_user_for_password(login: str, password: str):
    if login not in get_logins_from_user():
        return 2
    else:
        bd = sqlite3.connect(BASE)
        cur = bd.cursor()
        base_password = cur.execute("""SELECT password FROM user
                        WHERE login = ?""", (str(login),)).fetchall()
        bd.close()
        if password != base_password[0][0]:
            return 3
        else:
            print('ok')


def get_tables_from_table(login: str):
    bd = sqlite3.connect(BASE)
    cur = bd.cursor()
    tables = cur.execute("""SELECT table_items, bytes FROM [table]
                    WHERE login = ?""", (str(login),)).fetchall()
    bd.close()
    return tables[0]


def add_table(login: str, table_items: str, b: bytes):
    data = (str(login), str(table_items), b)
    bd = sqlite3.connect(BASE)
    cur = bd.cursor()
    cur.execute("""INSERT INTO [table](login, table_items, bytes) VALUES(?, ?, ?)""", data)
    bd.commit()
    bd.close()


source = wave.open("in.wav", mode="rb")

params = source.getparams()
frames = source.readframes(params.nframes)
params = tuple(params)
frames_count = params[3]

new_params = '-'.join(map(lambda x: str(x), list(params)))

source.close()

# add_table('Andr', new_params, frames)
# print(get_tables_from_table('Andr'))