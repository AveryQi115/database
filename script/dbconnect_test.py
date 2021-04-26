from MySQLdb import connect, OperationalError

dbaddress = "10.60.144.32"
dbname = "tjtdb"
username = "test"
password = "testtest"

try:
    conn = connect(dbaddress, username, password, dbname)
    pass
except OperationalError as identifier:
    print(str(identifier))
    pass
else:
    print("Connection Success")
    pass