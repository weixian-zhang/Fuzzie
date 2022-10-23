from datetime import datetime
import sqlalchemy
from sqlalchemy import *
import os
import json
from pathlib import Path
from models.webapi_fuzzcontext import ApiFuzzContext, ApiFuzzDataCase, ApiFuzzCaseSet, ApiFuzzRequest, ApiFuzzResponse
from eventstore import EventStore

evts = EventStore()

dbPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory/data/fuzzie.sqlite')
connStr = f'sqlite:///{dbPath}?check_same_thread=False'
engine = create_engine(connStr)
dbconn = engine.connect()

metadata = MetaData(engine)

apifuzzcontext_TableName = 'ApiFuzzContext'
apifuzzCaseSet_TableName = 'ApiFuzzCaseSet'
apifuzzDataCase_TableName = 'ApiFuzzDataCase'
apifuzzRequest_TableName = 'ApiFuzzRequest'
apifuzzResponse_TableName = 'ApiFuzzResponse'

FuzzContextTable = Table(apifuzzcontext_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('name', String),
                            Column('hostname', String),
                            Column('port', String),
                            Column('requestMessageSingle', String),
                            Column('requestMessageFilePath', String),
                            Column('openapi3FilePath', String),
                            Column('openapi3Url', String),
                            Column('fuzzMode', String),
                            Column('fuzzcaseToExec', Integer),
                            Column('authnType', String)
                            )
    
FuzzCaseSetTable = Table(apifuzzCaseSet_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('selected', Boolean),
                            Column('verb', String),
                            Column('path', String),
                            Column('querystringNonTemplate', String),
                            Column('bodyNonTemplate', String),
                            Column('pathDataTemplate', String, nullable=True),
                            Column('querystringDataTemplate', String, nullable=True),
                            Column('headerDataTemplate', String, nullable=True),
                            Column('bodyDataTemplate', String, nullable=True),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )


FuzzDataCaseTable = Table(apifuzzDataCase_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('progressState', String),
                            Column('fuzzCaseSetId', String, ForeignKey(f'{FuzzCaseSetTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{FuzzContextTable}.Id'))
                            )

FuzzRequestTable = Table(apifuzzRequest_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('hostnamePort', String),
                            Column('verb', String),
                            Column('path', String),
                            Column('querystring', String),
                            Column('url', String),
                            Column('headers', String),
                            Column('body', String),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{FuzzDataCaseTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{FuzzContextTable}.Id'))
                            )


FuzzResponseTable = Table(apifuzzResponse_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('statusCode', String),
                            Column('reasonPharse', String),
                            Column('responseJson', String),
                            Column('setcookieHeader', String),
                            Column('content', String),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{apifuzzResponse_TableName}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{FuzzContextTable}.Id'))
                            )

def get_fuzzcontexts() -> list[ApiFuzzContext]:
    j = FuzzContextTable.join(FuzzCaseSetTable,
                FuzzContextTable.c.Id == FuzzCaseSetTable.c.fuzzcontextId)
    stmt = select(FuzzContextTable, FuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"), FuzzCaseSetTable).select_from(j)
    results = dbconn.execute(stmt)
    fcRows = results.fetchall()
    
    if len(fcRows) == 0:
        return []
    
    fuzzcontexts = []
    
    for row in fcRows:
        
        rowDict = row._asdict()
        
        fuzzcontextId = rowDict['Id']

        yesno, existingFuzzContext = is_data_exist_in_fuzzcontexts(fuzzcontextId, fuzzcontexts)
        fuzzcontext = None
        if not yesno:
            fuzzcontext = create_fuzzcontext_from_dict(rowDict)
        else:
            fuzzcontext = existingFuzzContext
        
        fcs = create_fuzzcaseset_from_dict(rowDict)
        
        fuzzcontext.fuzzcaseSets.append(fcs)
        
        if not yesno:
            fuzzcontexts.append(fuzzcontext)
    
    return fuzzcontexts

def get_fuzzcontext(Id) -> ApiFuzzContext:
        j = FuzzContextTable.join(FuzzCaseSetTable,
                FuzzContextTable.c.Id == FuzzCaseSetTable.c.fuzzcontextId)
        stmt = (
                select(FuzzContextTable, FuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"), FuzzCaseSetTable)
                .where(FuzzContextTable.c.Id == Id)
                .select_from(j)
               )
        results = dbconn.execute(stmt)
        fcRows = results.fetchmany()
        
        if fcRows is None or len(fcRows) == 0:
            evts.emitErr(f'Cannot get fuzz context with Id: {Id}')
            return None
        
        singleRow = fcRows[0]._asdict()
        
        fuzzcontext = create_fuzzcontext_from_dict(singleRow)
        
        for row in fcRows:
            
            rowDict = row._asdict()
        
            fcs = create_fuzzcaseset_from_dict(rowDict)
            fuzzcontext.fuzzcaseSets.append(fcs)
            
        return fuzzcontext

def insert_db_fuzzcontext(fuzzcontext: ApiFuzzContext):
        
        fuzzcontextStmt = (
            insert(FuzzContextTable).
            values(
                   Id=fuzzcontext.Id, 
                   datetime=datetime.now(),
                   name = fuzzcontext.name,
                    hostname = fuzzcontext.hostname,
                    port = fuzzcontext.port,
                    fuzzMode = fuzzcontext.fuzzMode,
                    fuzzcaseToExec = fuzzcontext.fuzzcaseToExec,
                    authnType = fuzzcontext.authnType
                   )
         )
        
        dbconn.execute(fuzzcontextStmt)
        
        if len(fuzzcontext.fuzzcaseSets) > 0:
            for fcset in fuzzcontext.fuzzcaseSets:
                header = json.dumps(fcset.headerDataTemplate)
                body = json.dumps(fcset.bodyDataTemplate)
                
                fcSetStmt = (
                    insert(FuzzCaseSetTable).
                    values(
                        Id=fcset.Id, 
                        selected = fcset.selected,
                        verb = fcset.verb,
                        path = fcset.path,
                        querystringNonTemplate = fcset.querystringNonTemplate,
                        bodyNonTemplate = fcset.bodyNonTemplate,
                        pathDataTemplate = fcset.pathDataTemplate,
                        querystringDataTemplate = fcset.querystringDataTemplate,
                        headerDataTemplate = header,
                        bodyDataTemplate =  body,
                        fuzzcontextId = fuzzcontext.Id
                        )
                )
                
                dbconn.execute(fcSetStmt)
                
def insert_api_fuzzdatacase(fdc: ApiFuzzDataCase) -> None:
    stmt = (
            insert(FuzzDataCaseTable).
            values(
                    Id = fdc.Id,
                    fuzzCaseSetId = fdc.fuzzCaseSetId,
                    fuzzcontextId = fdc.fuzzcontextId,
                    progressState = fdc.progressState
                   )
         )
    dbconn.execute(stmt)

def insert_api_fuzzrequest(fr: ApiFuzzRequest) -> None:
    stmt = (
            insert(FuzzRequestTable).
            values(
                    Id = fr.Id,
                    datetime = fr.datetime,
                    fuzzDataCaseId = fr.fuzzDataCaseId,
                    fuzzcontextId = fr.fuzzcontextId,
                    hostnamePort = fr.hostnamePort,
                    verb = fr.verb,
                    path = fr.path,
                    querystring = fr.querystring,
                    url = fr.url,
                    headers = fr.headers,
                    body = fr.body
                   )
         )
    dbconn.execute(stmt)
    
def insert_api_fuzzresponse(fr: ApiFuzzResponse) -> None:
    stmt = (
            insert(FuzzResponseTable).
            values(
                    Id = fr.Id,
                    datetime = fr.datetime,
                    fuzzDataCaseId = fr.fuzzDataCaseId,
                    fuzzcontextId = fr.fuzzcontextId,
                    statusCode = fr.statusCode,
                    reasonPharse = fr.reasonPharse,
                    responseJson = fr.responseJson,
                    setcookieHeader = fr.setcookieHeader,
                    content = fr.content,

                   )
         )
    dbconn.execute(stmt)

# helpers
def is_data_exist_in_fuzzcontexts(fuzzcontextId: str, fuzzcontexts: list[ApiFuzzContext]):
        for fc in fuzzcontexts:
            if fc.Id == fuzzcontextId:
                return True, fc
        return False, None
    
def create_fuzzcontext_from_dict(rowDict):
        fuzzcontext = ApiFuzzContext()
        fuzzcontext.Id = rowDict['Id']
        fuzzcontext.datetime = rowDict['datetime']
        fuzzcontext.name = rowDict['name']
        
        fuzzcontext.requestMessageSingle = rowDict['requestMessageSingle']
        fuzzcontext.requestMessageFilePath = rowDict['requestMessageFilePath']
        fuzzcontext.openapi3FilePath = rowDict['openapi3FilePath']
        fuzzcontext.openapi3Url = rowDict['openapi3Url']
        
        fuzzcontext.hostname= rowDict['hostname']
        fuzzcontext.port= rowDict['port']
        fuzzcontext.fuzzMode= rowDict['fuzzMode']
        fuzzcontext.fuzzcaseToExec = rowDict['fuzzcaseToExec']
        fuzzcontext.authnType = rowDict['authnType']
        
        return fuzzcontext
    

def create_fuzzcaseset_from_dict(rowDict):
    fcs = ApiFuzzCaseSet()
    fcs.Id = rowDict['fuzzCaseSetId']
    fcs.path = rowDict['path']
    fcs.pathDataTemplate = rowDict['pathDataTemplate']
    fcs.querystringDataTemplate= rowDict['querystringDataTemplate']
    fcs.bodyDataTemplate= rowDict['bodyDataTemplate']
    fcs.headerDataTemplate = rowDict['headerDataTemplate']
    fcs.querystringNonTemplate = rowDict['querystringNonTemplate']
    fcs.bodyNonTemplate = rowDict['bodyNonTemplate']
    fcs.selected = rowDict['selected']
    fcs.verb = rowDict['verb']
    return fcs
                            
    
# create tables if not exist
metadata.create_all()


