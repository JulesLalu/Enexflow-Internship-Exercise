from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:Crefolet75$@localhost/db?host=localhost?port=3306"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""
app.config['MYSQL_DATABASE_SECURE_FILE_PRIV'] = ''
app.config['MYSQL_DATABASE_USER'] = '{}'.format(l2[0][1])
app.config['MYSQL_DATABASE_PASSWORD'] = '{}'.format(l2[1][1])
app.config['MYSQL_DATABASE_DB'] = '{}'.format(l2[2][1])
app.config['MYSQL_DATABASE_HOST'] = '{}'.format(l2[3][1])
mysql.init_app(app)
"""