import sqlite3
import threading

class Database:
    def __init__(self):
        self.lock=threading.RLock()
        self.conn=sqlite3.connect("Registry.db", check_same_thread=False)
        self.cursor=self.conn.cursor()
        with self.lock:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS paths(ID INTEGER PRIMARY KEY,App TEXT,Path TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS workspaces(ID INTEGER PRIMARY KEY,Workspace TEXT,Type TEXT,Resources TEXT,Browser TEXT) ")
            self.conn.commit()
    def store_path(self,app,path):
        with self.lock:
            self.cursor.execute("INSERT INTO paths(App,Path) VALUES(?,?)",(app,path))
            self.conn.commit()
    def check_path(self,app):
        with self.lock:
            self.cursor.execute("SELECT Path FROM paths WHERE App=?",(app,))
            path=self.cursor.fetchone()
        if path is None:
            return False
        else:
            return path[0]
    def store_workspace(self,workspace,type,resources,browser):
        with self.lock:
            self.cursor.execute("INSERT INTO workspaces(Workspace,Type,Resources,Browser) VALUES(?,?,?,?)",(workspace,type,resources,browser))
            self.conn.commit()
    def check_workspace(self,resource):
        with self.lock:
            self.cursor.execute("SELECT * FROM workspaces WHERE Resources=?",(resource,))
            Resources=self.cursor.fetchall()
        if not Resources:
            return False
        else:
            return Resources
    def load_workspace(self,workspace):
        with self.lock:
            self.cursor.execute("SELECT Resources,Type,Browser,ID FROM workspaces WHERE Workspace=?",(workspace,))
            resources=self.cursor.fetchall()
        return resources
    def delete_workspace(self,resource):
        with self.lock:
            self.cursor.execute("DELETE FROM workspaces WHERE ID=?",(resource,))
            self.conn.commit()
