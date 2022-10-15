import sqlalchemy
from sqlalchemy import *
from sqlalchemy.sql import select
import os
from pathlib import Path

dbPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory/data/fuzzie.sqlite')
#dbPath = dbPath.replace('\\','/')
connStr = f'sqlite:///{dbPath}'
engine = create_engine(connStr)
dbconn = engine.connect()

metadata = MetaData(engine)

apifuzzcontext_TableName = 'ApiFuzzContext'


api_fuzzcontex_table = Table(apifuzzcontext_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('name', String),
                            Column('hostname', String),
                            Column('port', String),
                            Column('fuzzMode', String),
                            Column('fuzzcaseToExec', Integer),
                            Column('authnType', String),
                            Column('isAnonymous', Boolean),
                            Column('basicUsername', String),
                            Column('basicPassword', String),
                            Column('bearerTokenHeader', String),
                            Column('bearerToken', String),
                            Column('apikeyHeader', String),
                            Column('apikey', String)
                            )


    # create table if not exist
metadata.create_all()
    
# if not engine.dialect.has_table(engine, table_name):
#    # Added to models.tables the new table I needed ( format Table as written above )
#    table_models = importlib.import_module('models.tables')

#    # Grab the class that represents the new table
#    # table_name = 'NewTableC'
#    ORMTable = getattr(table_models, table_name)            

#    # checkfirst=True to make sure it doesn't exists
#    ORMTable.__table__.create(bind=engine, checkfirst=True)


