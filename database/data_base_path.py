import sqlite3
class Recover:
    conn = sqlite3.connect("../src/modelo/database_management/todolist_db.db")
    def recovering(self):
        return self.conn
    def recover_cursor(self):
        return self.conn.cursor()
if __name__=='__main__':
    pass