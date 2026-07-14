import sqlite3

class Database:
    def __init__(self):
        self.conn=sqlite3.connect("Registry.db")
        self.cursor=self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS paths(ID INTEGER PRIMARY KEY,App TEXT,Path TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS workspaces(ID INTEGER PRIMARY KEY,Workspace TEXT,Type TEXT,Resources TEXT,Browser TEXT) ")
    def store_path(self,app,path):
        self.cursor.execute("INSERT INTO paths(App,Path) VALUES(?,?)",(app,path))
        self.conn.commit()
    def check_path(self,app):
        self.cursor.execute("SELECT Path FROM paths WHERE App=?",(app,))
        path=self.cursor.fetchone()
        if path is None:
            return False
        else:
            return path[0]
    def store_workspace(self,workspace,type,resources,browser):
        self.cursor.execute("INSERT INTO workspaces(Workspace,Type,Resources,Browser) VALUES(?,?,?,?)",(workspace,type,resources,browser))
        self.conn.commit()
    def check_workspace(self,resource):
        self.cursor.execute("SELECT * FROM workspaces WHERE Resources=?",(resource,))
        Resources=self.cursor.fetchall()
        if Resources is None:
            return False
        else:
            return Resources
    def load_workspace(self,workspace):
        self.cursor.execute("SELECT Resources,Type,Browser,ID FROM workspaces WHERE Workspace=?",(workspace,))
        resources=self.cursor.fetchall()
        return resources
    def delete_workspace(self,resource):
        self.cursor.execute("DELETE FROM workspaces WHERE ID=?",(resource,))
        self.conn.commit()