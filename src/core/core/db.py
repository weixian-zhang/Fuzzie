from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import *
from sqlalchemy.orm.exc import NoResultFound
import os
import json
from pathlib import Path
from models.webapi_fuzzcontext import (ApiFuzzContext, ApiFuzzDataCase, ApiFuzzCaseSet, ApiFuzzRequest, 
                                       ApiFuzzResponse,FuzzProgressState, ApiFuzzCaseSetRun
    )
from graphql_models import (ApiFuzzContext_Runs_ViewModel,
            ApiFuzzCaseSetRunViewModel, 
            ApiFuzzCaseSets_With_RunSummary_ViewModel)

from eventstore import EventStore

evts = EventStore()
dbPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory/data/fuzzie.sqlite')
connStr = f'sqlite:///{dbPath}?check_same_thread=False&_journal_mode=WAL'
engine = create_engine(connStr)

session_factory = sessionmaker(bind=engine)

metadata = MetaData(engine)

apifuzzcontext_TableName = 'ApiFuzzContext'
apifuzzCaseSet_TableName = 'ApiFuzzCaseSet'
apifuzzCaseSetRuns_TableName = 'ApiFuzzCaseSetRuns'
apifuzzDataCase_TableName = 'ApiFuzzDataCase'
apifuzzRequest_TableName = 'ApiFuzzRequest'
apifuzzResponse_TableName = 'ApiFuzzResponse'
apifuzzRunSummaryPerCaseSet_TableName = 'ApiFuzzRunSummaryPerCaseSetTable'

ApiFuzzContextTable = Table(apifuzzcontext_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('name', String),
                            Column('hostname', String),
                            Column('port', String),
                            Column('requestTextContent', String),
                            Column('requestTextFilePath', String),
                            Column('openapi3FilePath', String),
                            Column('openapi3Url', String),
                            Column('openapi3Content', String),
                            Column('fuzzcaseToExec', Integer),
                            Column('authnType', String),
                            Column('basicUsername', String),
                            Column('basicPassword', String),
                            Column('bearerTokenHeader', String),
                            Column('bearerToken', String),
                            Column('apikeyHeader', String),
                            Column('apikey', String)
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
                            Column('headerNonTemplate', String),
                            Column('pathDataTemplate', String, nullable=True),
                            Column('querystringDataTemplate', String, nullable=True),
                            Column('headerDataTemplate', String, nullable=True),
                            Column('bodyDataTemplate', String, nullable=True),
                            Column('progressState', String),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )

# track number of runs for each FuzzContext
# many to many mapping table
ApiFuzzCaseSetRunsTable= Table(apifuzzCaseSetRuns_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('startTime', DateTime),
                            Column('endTime', DateTime),
                            Column('status', String),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )

ApiFuzzRunSummaryPerCaseSetTable = Table(apifuzzRunSummaryPerCaseSet_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('http2xx', Integer),
                            Column('http3xx', Integer),
                            Column('http4xx', Integer),
                            Column('http5xx', Integer),
                            Column('completedDataCaseRuns', Integer),
                            Column('totalDataCaseRunsToComplete', Integer),
                            Column('fuzzCaseSetId', String, ForeignKey(f'{ApiFuzzCaseSetTable}.Id')),
                            Column('fuzzCaseSetRunId', String, ForeignKey(f'{ApiFuzzCaseSetRunsTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id'))
                            )

# RowNumber for pagination
ApiFuzzDataCaseTable = Table(apifuzzDataCase_TableName, metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Id', String),
                            Column('fuzzCaseSetId', String, ForeignKey(f'{ApiFuzzCaseSetTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id')),
                            Column('fuzzcaseSetRunIdId', String, ForeignKey(f'{apifuzzCaseSetRuns_TableName}.Id'))
                            )

# RowNumber for pagination
ApiFuzzRequestTable = Table(apifuzzRequest_TableName, metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Id', String),
                            Column('datetime', DateTime),
                            Column('hostnamePort', String),
                            Column('verb', String),
                            Column('path', String),
                            Column('querystring', String),
                            Column('url', String),
                            Column('headers', String),
                            Column('body', String),
                            Column('requestMessage', String),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{ApiFuzzDataCaseTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id'))
                            )

# RowNumber for pagination
ApiFuzzResponseTable = Table(apifuzzResponse_TableName, metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Id', String),
                            Column('datetime', DateTime),
                            Column('statusCode', String),
                            Column('reasonPharse', String),
                            Column('responseDisplayText', String),
                            Column('setcookieHeader', String),
                            Column('headerJson', String),
                            Column('body', String),
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
        
        fcRows = (Session.query(ApiFuzzContextTable, ApiFuzzContextTable.columns.Id.label("fuzzContextId"),
                                ApiFuzzCaseSetTable, ApiFuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"))
                  .select_from(join(ApiFuzzContextTable, ApiFuzzCaseSetTable))
                  .filter(ApiFuzzContextTable.c.Id == Id)
                  .filter(ApiFuzzCaseSetTable.c.selected.is_(fuzzCaseSetSelected))
                  .all()
                )
        
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

def get_fuzzContextSetRuns() -> list[ApiFuzzContext_Runs_ViewModel]:
    
    try:
        Session = scoped_session(session_factory)
        
        fcsRunRows = (
            Session.query
                    (
                        ApiFuzzContextTable.columns.Id.label("fuzzcontextId"), 
                        ApiFuzzContextTable.columns.datetime,
                        ApiFuzzContextTable.columns.name,
                        ApiFuzzContextTable.columns.requestMessageText,
                        ApiFuzzContextTable.columns.requestMessageFilePath,
                        ApiFuzzContextTable.columns.openapi3FilePath,
                        ApiFuzzContextTable.columns.openapi3Url,
                        ApiFuzzContextTable.columns.hostname,
                        ApiFuzzContextTable.columns.port,
                        ApiFuzzContextTable.columns.fuzzMode,      
                        ApiFuzzContextTable.columns.fuzzcaseToExec,
                        ApiFuzzContextTable.columns.authnType,
                        
                        ApiFuzzCaseSetRunsTable.columns.Id.label("fuzzCaseSetRunsId"),
                        ApiFuzzCaseSetRunsTable.columns.startTime,
                        ApiFuzzCaseSetRunsTable.columns.endTime,
                        ApiFuzzCaseSetRunsTable.columns.status
                        
                    )
                    #.join(ApiFuzzCaseSetTable, ApiFuzzCaseSetTable.columns.fuzzcontextId == ApiFuzzContextTable.columns.Id)
                    .join(ApiFuzzCaseSetRunsTable, ApiFuzzCaseSetRunsTable.columns.fuzzcontextId == ApiFuzzContextTable.columns.Id, isouter=True)
                    .all()
        )
            
        
        fcViews = {}
               
        fcidProcessed = set()
        # get first row for FuzzContext as its fields are repeated
        for row in fcsRunRows:
            
           rowDict = row._asdict()
           
           fcid = rowDict['fuzzcontextId']
           
           if not fcid in fcidProcessed:
            
                fcidProcessed.add(fcid) 
                
                fcView = ApiFuzzContext_Runs_ViewModel()
                fcView.Id = rowDict['fuzzcontextId']
                fcView.datetime = rowDict['datetime']
                fcView.name = rowDict['name']
                fcView.requestMessageText = rowDict['requestMessageText']
                fcView.requestMessageFilePath = rowDict['requestMessageFilePath']
                fcView.openapi3FilePath = rowDict['openapi3FilePath']
                fcView.openapi3Url = rowDict['openapi3Url']
                fcView.hostname = rowDict['hostname']
                fcView.port = rowDict['port']
                fcView.fuzzMode = rowDict['fuzzMode']   
                fcView.fuzzcaseToExec = rowDict['fuzzcaseToExec']
                fcView.authnType = rowDict['authnType']
                fcView.fuzzCaseSetRuns = []
                
                fcViews[fcid] = fcView
           
           fcsRunId = rowDict['fuzzCaseSetRunsId']
           #outer join causing "empty" records to also create, ignore empty FuzzCaseSetRun records
           if fcsRunId == None:
               continue
           
           fcRunView = ApiFuzzCaseSetRunViewModel()
           fcRunView.fuzzCaseSetRunsId = fcsRunId
           fcRunView.fuzzcontextId = rowDict['fuzzcontextId']
           fcRunView.startTime = rowDict['startTime']
           fcRunView.endTime =  rowDict['endTime']
           fcRunView.status = rowDict['status']
           
           fcView = fcViews[fcRunView.fuzzcontextId]
           fcView.fuzzCaseSetRuns.append(fcRunView)
           
           
        fcList = []
        
        for x in fcViews.keys():
            fcList.append(fcViews[x])
        
        
        return fcList
        
    except Exception as e:
        print(e)
    finally:
        Session.close()
        

def get_caseSets_with_runSummary(fuzzcontextId):
    
    Session = scoped_session(session_factory)
        
    fcsSumRows = (Session.query(ApiFuzzCaseSetTable, ApiFuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"),
                            ApiFuzzCaseSetTable.columns.fuzzcontextId.label("fuzzcontextId"),
                            ApiFuzzRunSummaryPerCaseSetTable.columns.http2xx,
                            ApiFuzzRunSummaryPerCaseSetTable.columns.http3xx,
                            ApiFuzzRunSummaryPerCaseSetTable.columns.http4xx,
                            ApiFuzzRunSummaryPerCaseSetTable.columns.http5xx,
                            ApiFuzzRunSummaryPerCaseSetTable.columns.completedDataCaseRuns,
                            ApiFuzzRunSummaryPerCaseSetTable.columns.totalDataCaseRunsToComplete,
                            ApiFuzzRunSummaryPerCaseSetTable.columns.Id.label("runSummaryId"),
                            ApiFuzzRunSummaryPerCaseSetTable.columns.fuzzCaseSetRunId
                            )
                .filter(ApiFuzzCaseSetTable.c.fuzzcontextId == fuzzcontextId)
                .join(ApiFuzzRunSummaryPerCaseSetTable, ApiFuzzCaseSetTable.columns.Id == ApiFuzzRunSummaryPerCaseSetTable.columns.fuzzCaseSetId, isouter=True)
                .all()
            )
        
    Session.close()
    
    result = []
    
    for row in fcsSumRows:
        
        rowDict = row._asdict()
        
        fcsSum = ApiFuzzCaseSets_With_RunSummary_ViewModel()
    
        fcsSum.fuzzCaseSetId = rowDict['fuzzCaseSetId']
        fcsSum.fuzzCaseSetRunId = rowDict['fuzzCaseSetRunId']
        fcsSum.fuzzcontextId = rowDict['fuzzcontextId']
        fcsSum.selected = rowDict['selected']
        fcsSum.verb = rowDict['verb']
        fcsSum.path = rowDict['path']
        fcsSum.querystringNonTemplate = rowDict['querystringNonTemplate']
        fcsSum.bodyNonTemplate = rowDict['bodyNonTemplate']
        fcsSum.headerNonTemplate = rowDict['headerNonTemplate']
        
        summaryId = rowDict['runSummaryId']
        
        if not summaryId is None:
            fcsSum.runSummaryId = summaryId
            fcsSum.http2xx = rowDict['http2xx']
            fcsSum.http3xx = rowDict['http3xx']
            fcsSum.http4xx = rowDict['http4xx']
            fcsSum.http5xx = rowDict['http5xx']
            fcsSum.completedDataCaseRuns = rowDict['completedDataCaseRuns']
            fcsSum.totalDataCaseRunsToComplete = rowDict['totalDataCaseRunsToComplete']
        
        result.append(fcsSum)
    
    return result



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
    


# mutations
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
                    requestTextContent = fuzzcontext.requestTextContent,
                    requestTextFilePath = fuzzcontext.requestTextFilePath,
                    openapi3FilePath = fuzzcontext.openapi3FilePath,
                    openapi3Url = fuzzcontext.openapi3Url,
                    openapi3Content = fuzzcontext.openapi3Content,
                    authnType = fuzzcontext.authnType,
                    basicUsername = fuzzcontext.basicUsername,
                    basicPassword = fuzzcontext.basicPassword,
                    bearerTokenHeader = fuzzcontext.basicPassword,
                    bearerToken = fuzzcontext.bearerToken,
                    apikeyHeader = fuzzcontext.apikeyHeader,
                    apikey = fuzzcontext.apikey
                   )
         )
        
        Session.execute(fuzzcontextStmt)
        
        # insert fuzzcasesets
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
                        headerNonTemplate = fcset.headerNonTemplate,
                        bodyDataTemplate =  body,
                        fuzzcontextId = fuzzcontext.Id
                        )
                )
                
                Session.execute(fcSetStmt)
        
        Session.commit()
        Session.close()

def insert_api_fuzzCaseSetRuns(Id, fuzzcontextId) -> None:
    stmt = (
            insert(ApiFuzzCaseSetRunsTable).
            values(
                    Id = Id,
                    startTime = datetime.now(),
                    status = 'fuzzing',
                    fuzzcontextId = fuzzcontextId
                   )
         )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
    
def update_api_fuzzCaseSetRun_status(fuzzCaseSetRunId, status = 'completed') -> None:
    stmt = (
            update(ApiFuzzCaseSetRunsTable).
            where(ApiFuzzCaseSetRunsTable.c.Id == fuzzCaseSetRunId).
            values(
                    endTime = datetime.now(),
                    status = status
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
    
    if fr.Id is None:
        raise Exception('ApiFuzzRequest is None while persisting')
                        
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
                    body = fr.body,
                    requestMessage = fr.requestMessage
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
                    responseDisplayText = fr.responseDisplayText,
                    setcookieHeader = fr.setcookieHeader,
                    headerJson = fr.headerJson,
                    body = fr.body,
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
        fuzzcontext.Id = rowDict['fuzzContextId']
        fuzzcontext.datetime = rowDict['datetime']
        fuzzcontext.name = rowDict['name']
        
        fuzzcontext.requestMessageText = rowDict['requestMessageText']
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


def create_casesetrun_summary(Id, fuzzCaseSetId, fuzzCaseSetRunId, fuzzcontextId, totalRunsToComplete=1):
    
    stmt = (
            insert(ApiFuzzRunSummaryPerCaseSetTable).
            values(
                    Id=Id,
                    http2xx = 0,
                    http3xx = 0,
                    http4xx = 0,
                    http5xx = 0,
                    completedDataCaseRuns = 0,
                    totalDataCaseRunsToComplete = totalRunsToComplete,
                    fuzzCaseSetId = fuzzCaseSetId,
                    fuzzCaseSetRunId=fuzzCaseSetRunId,
                    fuzzcontextId=fuzzcontextId
                   )
         )

    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
    
def update_casesetrun_summary(Id, httpCode, completedDataCaseRuns = 0) -> ApiFuzzCaseSets_With_RunSummary_ViewModel :
    
    Session = scoped_session(session_factory)

    summary = (
                Session
                .query(ApiFuzzRunSummaryPerCaseSetTable)
                .filter(ApiFuzzRunSummaryPerCaseSetTable.c.Id == Id)
                .first()
               )
    rowDict =  summary._asdict()
    existingHttp2xx = rowDict['http2xx']
    existingHttp3xx = rowDict['http3xx']
    existingHttp4xx = rowDict['http4xx']
    existingHttp5xx = rowDict['http5xx']
    existingCompletedDataCaseRuns = rowDict['completedDataCaseRuns']
    
    if httpCode >= 200 and httpCode <= 299:
        existingHttp2xx = existingHttp2xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == Id).
            values(
                    http2xx = existingHttp2xx
                   )
            )
        Session.execute(stmt)
    
    elif httpCode >= 300 and httpCode <= 399:
        existingHttp3xx = existingHttp3xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == Id).
            values(
                    http3xx = existingHttp3xx
                   )
            )
        Session.execute(stmt)
    
    elif httpCode >= 400 and httpCode <= 499:
        existingHttp4xx = existingHttp4xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == Id).
            values(
                    http4xx = existingHttp4xx
                   )
            )
        Session.execute(stmt)
        
    elif httpCode >= 500 and httpCode <= 599:
        existingHttp5xx = existingHttp5xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == Id).
            values(
                    http5xx = existingHttp5xx
                   )
            )
        Session.execute(stmt)
        
    # +1 to completed run
    existingCompletedDataCaseRuns = existingCompletedDataCaseRuns + completedDataCaseRuns
    stmt = (
        update(ApiFuzzRunSummaryPerCaseSetTable).
        where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == Id).
        values(
                completedDataCaseRuns = existingCompletedDataCaseRuns
                )
        )
    Session.execute(stmt)
        
    Session.commit()
    Session.close()
    
    summary = ApiFuzzCaseSet_RunSummary_ViewModel()
    summary.Id = Id
    summary.http2xx = existingHttp2xx
    summary.http3xx = existingHttp3xx
    summary.http4xx = existingHttp4xx
    summary.http5xx = existingHttp5xx
    summary.completedDataCaseRuns = existingCompletedDataCaseRuns
    return summary
        
               
    
# create tables if not exist
metadata.create_all()


