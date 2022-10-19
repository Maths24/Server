import mysql.connector



class DBController:
    def __init__(self) -> None:
        print("database started")
        #Verbindung zu Datenbank herstellen
        self.mydb = mysql.connector.connect (
        host = "localhost",
        user = "root",
        password = "himbeertorteDB",
        database="kundenzaehler")

        self.mycursor = self.mydb.cursor()
   
    def query(self, query=""):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
