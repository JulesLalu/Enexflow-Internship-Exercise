from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

with open("id_info.txt") as b_file :
    str=b_file.read()
    l2 = str.split("\n")
    for i in range(len(l2)) :
        l2[i]=l2[i].split(" : ")
    

# MySQL configurations
app.config['MYSQL_DATABASE_SECURE_FILE_PRIV'] = ''
app.config['MYSQL_DATABASE_USER'] = '{}'.format(l2[0][1])
app.config['MYSQL_DATABASE_PASSWORD'] = '{}'.format(l2[1][1])
app.config['MYSQL_DATABASE_DB'] = '{}'.format(l2[2][1])
app.config['MYSQL_DATABASE_HOST'] = '{}'.format(l2[3][1])
mysql.init_app(app)