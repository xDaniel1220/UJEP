from sqlalchemy import create_engine
# for postgreSQL database credentials can be written as 
user = 'daniel.blaha'
password = ''
host = 'localhost'
port = '5432'
database = 'starfield'
# for creating connection string
connection_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
# SQLAlchemy engine
engine = create_engine(connection_str)
# you can test if the connection is made or not
try:
    with engine.connect() as connection_str:
        print('Successfully connected to the PostgreSQL database')
except Exception as ex:
    print(f'Sorry failed to connect: {ex}')