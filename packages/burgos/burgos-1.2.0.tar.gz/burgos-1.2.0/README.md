# Session
### Usage:
```python
from burgos.session import Session
session = Session(database_auth, login_table)
```

database_auth: json/dict
```json
{
    "host": "host ip address or domain",
    "database": "database name",
    "user": "username",
    "password": "user password"
}
```

login_table: string
```
"table_name_which_contains_login_data"
```

### Built-in methods

##### database.reconnectDatabase()
- reconnects to the database

##### getConnection(ip)
- ip = string containing an ip address
- returns the connection matching the selected ip address
- if there is no connection with that ip, returns None

##### login(user, password, ip)
- user = string containing the username, email or cpf as login method
- password = string containg the password
- ip = string containing an ip address
- if "user" is number only, it will be checked as cpf
- if "user" has an "@", it will be checked as an email
- if "user" is neither, it will be checked as an username
- if there is a row in database.login_table that matches with this user and password, a Connection will be instanciated and the user id will be returned

# Mysql
### Usage:
```python
from burgos.mysql_handler import Mysql
database = Mysql(login_table)
```

login_table: string
```
"table_name_which_contains_login_data"
```

### Built-in methods

##### connect(auth:dict)
- auth = dictionary containing authentication data (same as session's database_auth)
- connects to the database and must be called before any other method (session already calls this in it's constructor)

##### disconnect()
- disconnects from the database

##### run(sql)
- sql = string containing SQL code
- sql code will be executed and commited into the database
- if sql first word, lowered, is equal to "select", this method will return a list containing the selected rows

##### fetchTable(table, rows = 0, where = [], reversed = None, ordered = None)
- table = string containing the table name which should be selected data from
- rows = int number that means the number of rows that should be selected. Optional (default: all rows)
- where = list containing strings which are the column and value. Ex.: where = ["username", "nandobfer"]. Optional.
- reversed = boolean indicating if the where query should be reversed or not. Optional.
- ordered = string containing the "ORDER BY" information. Ex. ordered = "id" / ordered = "datetime DESC"
- Returns a list containing another list for each row fetched. Returns an empty list if there was none.