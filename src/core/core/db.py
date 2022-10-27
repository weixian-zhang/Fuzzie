from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import *
from sqlalchemy.orm.exc import NoResultFound
import os
import json
from pathlib import Path
from models.webapi_fuzzcontext import ApiFuzzContext, ApiFuzzDataCase, ApiFuzzCaseSet, ApiFuzzRequest, ApiFuzzResponse,FuzzProgressState, ApiFuzzCaseSetRun
from eventstore import EventStore

evts = EventStore()

dbPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory/data/fuzzie.sqlite')
connStr = f'sqlite:///{dbPath}?check_same_thread=False'
engine = create_engine(connStr)

session_factory = sessionmaker(bind=engine)


metadata = MetaData(engine)

apifuzzcontext_TableName = 'ApiFuzzContext'
apifuzzCaseSet_TableName = 'ApiFuzzCaseSet'
apifuzzCaseSetRuns_TableName = 'ApiFuzzCaseSetRuns'
apifuzzDataCase_TableName = 'ApiFuzzDataCase'
apifuzzRequest_TableName = 'ApiFuzzRequest'
apifuzzResponse_TableName = 'ApiFuzzResponse'

ApiFuzzContextTable = Table(apifuzzcontext_TableName, metadata,
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
# Api schema, or see this as a "Api schema template" for execution
# When fuzz executes based on this FuzzCaseSet template, the result is a list of 1 ApiFuzzCaseSetRun -> many ApiFuzzDataCases
ApiFuzzCaseSetTable = Table(apifuzzCaseSet_TableName, metadata,
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
                            Column('progressState', String),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )

# track number of runs for each FuzzContext
# many to many mapping table
ApiFuzzCaseSetRuns= Table(apifuzzCaseSetRuns_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('startTime', DateTime),
                            Column('endTime', DateTime),
                            Column('completed', Boolean),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )


ApiFuzzDataCaseTable = Table(apifuzzDataCase_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('fuzzCaseSetId', String, ForeignKey(f'{ApiFuzzCaseSetTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id')),
                            Column('fuzzcaseSetRunIdId', String, ForeignKey(f'{apifuzzCaseSetRuns_TableName}.Id'))
                            )

ApiFuzzRequestTable = Table(apifuzzRequest_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('hostnamePort', String),
                            Column('verb', String),
                            Column('path', String),
                            Column('querystring', String),
                            Column('url', String),
                            Column('headers', String),
                            Column('body', String),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{ApiFuzzDataCaseTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id'))
                            )


ApiFuzzResponseTable = Table(apifuzzResponse_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('statusCode', String),
                            Column('reasonPharse', String),
                            Column('responseJson', String),
                            Column('setcookieHeader', String),
                            Column('content', String),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{apifuzzResponse_TableName}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id'))
                            )

NaughtyPasswordTable = Table('NaughtyPassword', metadata,
                            Column('id', String, primary_key=True),
                            Column('Content', String),
                            Column('RowNumber', String)
                            )

NaughtyUsernameTable = Table('NaughtyUsername', metadata,
                            Column('id', String, primary_key=True),
                            Column('Content', String),
                            Column('RowNumber', String)
                            )

NaughtyStringTable = Table('NaughtyString', metadata,
                            Column('id', String, primary_key=True),
                            Column('Content', String),
                            Column('RowNumber', String)
                            )


def get_fuzzcontexts() -> list[ApiFuzzContext]:
    j = ApiFuzzContextTable.join(ApiFuzzCaseSetTable,
                ApiFuzzContextTable.c.Id == ApiFuzzCaseSetTable.c.fuzzcontextId)
    stmt = select(ApiFuzzContextTable, ApiFuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"), ApiFuzzCaseSetTable).select_from(j)
    
    Session = scoped_session(session_factory)
        
    results = Session.execute(stmt)
        
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
    
    Session.close()
    
    return fuzzcontexts

def get_fuzzcontext(Id, fuzzCaseSetSelected = True) -> ApiFuzzContext:       
        
        Session = scoped_session(session_factory)
        
        fcRows = (Session.query(ApiFuzzContextTable, ApiFuzzCaseSetTable, ApiFuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"))
                  .select_from(join(ApiFuzzContextTable, ApiFuzzCaseSetTable))
                  .filter(ApiFuzzContextTable.c.Id == Id)
                  .filter(ApiFuzzCaseSetTable.c.selected.is_(fuzzCaseSetSelected))
                  .all()
                )
        
        
        # results = Session.execute(stmt)
        
        # fcRows = results.fetchmany()
        
        Session.close()
        
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

        Session = scoped_session(session_factory)
        
        fuzzcontextStmt = (
            insert(ApiFuzzContextTable).
            values(
                   Id=fuzzcontext.Id, 
                   datetime= datetime.now(),
                   name = fuzzcontext.name,
                    hostname = fuzzcontext.hostname,
                    port = fuzzcontext.port,
                    fuzzMode = fuzzcontext.fuzzMode,
                    fuzzcaseToExec = fuzzcontext.fuzzcaseToExec,
                    authnType = fuzzcontext.authnType
                   )
         )
        
        Session.execute(fuzzcontextStmt)
        
        # insert fuzzcaseset
        
        if len(fuzzcontext.fuzzcaseSets) > 0:
            for fcset in fuzzcontext.fuzzcaseSets:
                header = json.dumps(fcset.headerDataTemplate)
                body = json.dumps(fcset.bodyDataTemplate)
                
                fcSetStmt = (
                    insert(ApiFuzzCaseSetTable).
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
                
                Session.execute(fcSetStmt)
        
        Session.commit()
        Session.close()

def insert_api_fuzzCaseSetRuns(Id, fuzzcontextId) -> None:
    stmt = (
            insert(ApiFuzzCaseSetRuns).
            values(
                    Id = Id,
                    startTime = datetime.now(),
                    completed = False,
                    fuzzcontextId = fuzzcontextId
                   )
         )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
    
def update_api_fuzzCaseSetRun_completed(fuzzCaseSetRunId) -> None:
    stmt = (
            update(ApiFuzzCaseSetRuns).
            where(ApiFuzzCaseSetRuns.c.Id == fuzzCaseSetRunId).
            values(
                    endTime = datetime.now(),
                    completed = True
                   )
            )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
                
def insert_api_fuzzdatacase(fuzzCaseSetRunId, fdc: ApiFuzzDataCase) -> None:
    stmt = (
            insert(ApiFuzzDataCaseTable).
            values(
                    Id = fdc.Id,
                    fuzzcaseSetRunIdId = fuzzCaseSetRunId,
                    fuzzCaseSetId = fdc.fuzzCaseSetId,
                    fuzzcontextId = fdc.fuzzcontextId
                   )
         )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
    
def insert_api_fuzzrequest(fr: ApiFuzzRequest) -> None:
    stmt = (
            insert(ApiFuzzRequestTable).
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
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
    
def insert_api_fuzzresponse(fr: ApiFuzzResponse) -> None:
    stmt = (
            insert(ApiFuzzResponseTable).
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

    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()

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

def get_naughtypassword_by_id(id):
    
        
    Session = scoped_session(session_factory)
    
    row = Session.query(NaughtyPasswordTable.columns.Content).filter(NaughtyPasswordTable.c.id == id).one()
    
    Session.close()
        
    rowDict = row._asdict()
    
    return rowDict['Content']

def get_naughtypassword_row_count():
    Session = scoped_session(session_factory)
    
    count = Session.query(NaughtyPasswordTable.c.id).count()
    
    Session.close()
    
    return count


def get_naughtyusername_by_id(id) -> str:
    
        
    Session = scoped_session(session_factory)
    
    row = Session.query(NaughtyUsernameTable.columns.Content).filter(NaughtyUsernameTable.c.id == id).one()
    
    Session.close()
        
    rowDict = row._asdict()
    
    return rowDict['Content']

def get_naughtyusername_row_count():
    Session = scoped_session(session_factory)
    
    count = Session.query(NaughtyUsernameTable.c.id).count()
    
    Session.close()
    
    return count

def get_naughtystring_by_id(id) -> str:
    
    try:
        Session = scoped_session(session_factory)

        row = Session.query(NaughtyStringTable.columns.Content).filter(NaughtyStringTable.c.id == id).one()
        
        Session.close()
        
        rowDict = row._asdict()
        
        return rowDict['Content']
    
    except NoResultFound as e:
        print(e)
    

def get_naughtystring_row_count():
    Session = scoped_session(session_factory)
    
    count = Session.query(NaughtyStringTable.c.id).count()
    
    Session.close()
    
    return count


def update_fuzzcaseset_fuzzing_in_progress(fuzzCaseSetId):
    pass

def update_fuzzcaseset_fuzzing_completed(fuzzCaseSetId):
    pass

def update_fuzzcaseset_fuzzing_stop(fuzzCaseSetId):
    pass

                            
    
# create tables if not exist
metadata.create_all()


