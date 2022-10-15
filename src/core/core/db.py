from datetime import datetime
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
apifuzzCaseSet_TableName = 'ApiFuzzCaseSet'
apifuzzDataCase_TableName = 'ApiFuzzDataCase'
apifuzzRequest_TableName = 'ApiFuzzRequest'
apifuzzResponse_TableName = 'ApiFuzzResponse'

api_fuzzcontext_table = Table(apifuzzcontext_TableName, metadata,
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
    
api_fuzzcaseset_table = Table(apifuzzCaseSet_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('selected', Boolean),
                            Column('verb', String),
                            Column('pathDataTemplate', String, nullable=True),
                            Column('querystringDataTemplate', String, nullable=True),
                            Column('headerDataTemplate', String, nullable=True),
                            Column('cookieDataTemplate', String, nullable=True),
                            Column('bodyDataTemplate', String, nullable=True),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )


api_fuzzdatacase_table = Table(apifuzzDataCase_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('fuzzCaseSetId', Integer, ForeignKey(f'{apifuzzDataCase_TableName}.Id')),
                            )

api_fuzzRequest_table = Table(apifuzzRequest_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('path', String),
                            Column('querystring', String),
                            Column('url', String),
                            Column('headers', String),
                            Column('cookies', Integer),
                            Column('body', String),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{api_fuzzdatacase_table}.Id'))
                            )

api_fuzzResponse_table = Table(apifuzzResponse_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('statusCode', String),
                            Column('reasonPharse', String),
                            Column('headers', String),
                            Column('body', String),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{apifuzzResponse_TableName}.Id'))
                            )
                            
    
# create tables if not exist
metadata.create_all()


