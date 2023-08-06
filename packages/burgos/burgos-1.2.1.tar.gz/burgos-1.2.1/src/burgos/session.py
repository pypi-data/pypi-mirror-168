from datetime import datetime, timedelta, date
from burgos.mysql_handler import Mysql


class Connection():
    def __init__(self, ip, database, id):
        self.id = id
        self.ip = ip
        self.expira = datetime.now() + timedelta(minutes=15)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True

class Session():
    def __init__(self, database_auth:dict, login_table):
        self.connections = []
        self.database_auth = database_auth
        self.database = Mysql(database_auth, login_table)

    def getConnection(self, ip):
        for connection in self.connections:
            if connection.ip == ip:
                if not connection.isExpired():
                    return connection
                else:
                    self.connections.remove(connection)

    def login(self, user, password, ip):
        self.database.connect()
        cpf = None
        email = None
        try:
            cpf = int(user)
        except:
            pass
        
        if '@' in user:
            email = True
        
        if cpf:
            column = 'cpf'
        elif email:
            column = 'email'
        else:
            column = 'usuario'
        
        try:
            data = self.database.fetchTable(1, self.database.login_table, column, user)[0]
            if data:
                if password == data[2]:
                    id = data[0]

                    # check if user is already logged and update it' connection if it exists
                    is_logged = self.getConnection(ip)
                    if is_logged and is_logged.id == id:
                        self.connections.remove(is_logged)

                    self.connections.append(
                        Connection(ip, self.database, id))
                    self.database.connect()
                    return str(id)
        except Exception as error:
            print(error)
            self.database.connect()
            return None
