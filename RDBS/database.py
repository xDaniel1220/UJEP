from sqlalchemy import create_engine, select, MetaData, Table, Column, Integer, String

user = 'daniel.blaha'
password = ''
host = 'localhost'
port = '5432'
database = 'starfield'

connection_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_str)
metadata_obj = MetaData()

try:
    with engine.connect() as connection:
        print('Successfully connected to the PostgreSQL database.')
except Exception as ex:
    print(f'Sorry failed to connect: {ex}')

table = Table(
    "systemy",
    metadata_obj,
    Column("id_systemy", Integer, primary_key=True),
    Column("nazev", String(50))
)

stmt = select(table).where(table.c.nazev == "Sol")
print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)





