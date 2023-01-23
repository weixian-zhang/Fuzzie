from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import *
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.pool import StaticPool
import os
import json
from pathlib import Path
from models.webapi_fuzzcontext import (ApiFuzzContext, ApiFuzzDataCase, ApiFuzzCaseSet, ApiFuzzRequest, 
                                       ApiFuzzResponse,FuzzProgressState, ApiFuzzCaseSetRun
    )
from graphql_models import (ApiFuzzContext_Runs_ViewModel,
            ApiFuzzCaseSetRunViewModel, 
            ApiFuzzCaseSets_With_RunSummary_ViewModel,
            ApiFuzzContextUpdate)

from utils import Utils
from eventstore import EventStore

eventstore = EventStore()
dbPath = os.path.join(os.path.dirname(Path(__file__)), 'corporafactory/data/fuzzie.sqlite')
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
apifuzzRequestFileUpload_TableName = 'ApiFuzzRequestFileUpload'
apifuzzRunSummaryPerCaseSet_TableName = 'ApiFuzzRunSummaryPerCaseSetTable'

ApiFuzzContextTable = Table(apifuzzcontext_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('datetime', DateTime),
                            Column('name', String),
                            Column('hostname', String),
                            Column('port', Integer),
                            Column('apiDiscoveryMethod', String),
                            Column('requestTextContent', String),
                            Column('requestTextFilePath', String),
                            Column('openapi3FilePath', String),
                            Column('openapi3Url', String),
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
                            Column('hostname', String),
                            Column('port', Integer),
                            Column('verb', String),
                            Column('path', String),
                            Column('querystringNonTemplate', String),
                            Column('bodyNonTemplate', String),
                            Column('headerNonTemplate', String),
                            Column('pathDataTemplate', String, nullable=True),
                            Column('querystringDataTemplate', String, nullable=True),
                            Column('headerDataTemplate', String, nullable=True),
                            Column('bodyDataTemplate', String, nullable=True),
                            Column('file', String),
                            Column('fileDataTemplate', String),
                            Column('requestMessage', String),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )

# track number of runs for each FuzzContext
# many to many mapping table
ApiFuzzCaseSetRunsTable= Table(apifuzzCaseSetRuns_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('startTime', DateTime),
                            Column('endTime', DateTime),
                            Column('status', String),
                            Column('message', String),
                            Column('fuzzcontextId', String, ForeignKey(f'{apifuzzcontext_TableName}.Id'))
                            )

ApiFuzzRunSummaryPerCaseSetTable = Table(apifuzzRunSummaryPerCaseSet_TableName, metadata,
                            Column('Id', String, primary_key=True),
                            Column('http2xx', Integer, default=0), 
                            Column('http3xx', Integer, default=0),
                            Column('http4xx', Integer, default=0),
                            Column('http5xx', Integer, default=0),
                            Column('completedDataCaseRuns', Integer, default=0),
                            Column('totalDataCaseRunsToComplete', Integer, default=0),
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
                            Column('fuzzCaseSetRunId', String, ForeignKey(f'{apifuzzCaseSetRuns_TableName}.Id'))
                            )

# RowNumber for pagination
ApiFuzzRequestTable = Table(apifuzzRequest_TableName, metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Id', String),
                            Column('datetime', DateTime),
                            Column('hostname', String),
                            Column('port', Integer),
                            Column('hostnamePort', String),
                            Column('verb', String),
                            Column('path', String),
                            Column('querystring', String),
                            Column('url', String),
                            Column('headers', String),
                            Column('body', String),
                            Column('invalidRequestError', String),
                            Column('requestMessage', String),
                            Column('contentLength', Integer),
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
                            Column('contentLength', Integer),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{apifuzzResponse_TableName}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id'))
                            )

# RowNumber for pagination
ApiFuzzRequestFileUploadTable = Table(apifuzzRequestFileUpload_TableName, metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Id', String),
                            Column('datetime', DateTime),
                            Column('wordlist_type', String),
                            Column('fileName', String),
                            Column('fileContent', String),
                            Column('fuzzRequestId', String, ForeignKey(f'{ApiFuzzRequestTable}.Id')),
                            Column('fuzzDataCaseId', String, ForeignKey(f'{ApiFuzzDataCaseTable}.Id')),
                            Column('fuzzcontextId', String, ForeignKey(f'{ApiFuzzContextTable}.Id')))


RandomImageTable = Table('RandomImage', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Content', String)
                            )
SeclistPasswordTable = Table('SeclistPassword', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Content', String)
                            )
SeclistUsernameTable = Table('SeclistUsername', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Content', String)
                            )
SeclistBLNSTable = Table('SeclistBLNS', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Content', String)
                            )
SeclistXSSTable = Table('SeclistXSS', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Content', String)
                            )
SeclistSqlInjectionTable = Table('SeclistSqlInjection', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Content', String)
                            )
SeclistPayloadTable = Table('SeclistPayload', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Filename', String),
                            Column('Content', String)
                            )
SeclistCharTable = Table('SeclistChar', metadata,
                            Column('RowNumber', Integer, primary_key=True),
                            Column('Content', String)
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
    
    Session.commit()
    Session.close()
    
    return fuzzcontexts

# gets the fuzz-context for fuzzing with option to select only FuzzCaseSet marked with 'selected'
def get_fuzzcontext(Id, fuzzCaseSetSelected = True) -> ApiFuzzContext:       
        
        Session = scoped_session(session_factory)
        
        fcRows = (Session.query(ApiFuzzContextTable, ApiFuzzContextTable.columns.Id.label("fuzzContextId"),
                                ApiFuzzCaseSetTable, ApiFuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"))
                  .select_from(join(ApiFuzzContextTable, ApiFuzzCaseSetTable))
                  .filter(ApiFuzzContextTable.c.Id == Id)
                  .filter(ApiFuzzCaseSetTable.c.selected.is_(fuzzCaseSetSelected))
                  .all()
                )
        
        Session.commit()
        Session.close()
        
        # None can means FuzzCaseSet is unselected
        if fcRows is None or len(fcRows) == 0:
            return None
        
        singleRow = fcRows[0]._asdict()
        
        fuzzcontext = create_fuzzcontext_from_dict(singleRow)
        
        for row in fcRows:
            
            rowDict = row._asdict()
        
            fcs = create_fuzzcaseset_from_dict(rowDict)
            fuzzcontext.fuzzcaseSets.append(fcs)
        
        return fuzzcontext

def get_fuzzContexts_and_runs() -> list[ApiFuzzContext_Runs_ViewModel]:
    
    try:
        Session = scoped_session(session_factory)
        
        fcsRunRows = (
            Session.query
                    (
                        ApiFuzzContextTable.columns.Id.label("fuzzcontextId"), 
                        ApiFuzzContextTable.columns.datetime,
                        ApiFuzzContextTable.columns.apiDiscoveryMethod,  
                        ApiFuzzContextTable.columns.name,
                        ApiFuzzContextTable.columns.requestTextContent,
                        ApiFuzzContextTable.columns.requestTextFilePath,
                        ApiFuzzContextTable.columns.openapi3FilePath,
                        ApiFuzzContextTable.columns.openapi3Url,
                        ApiFuzzContextTable.columns.basicUsername,
                        ApiFuzzContextTable.columns.basicPassword,
                        ApiFuzzContextTable.columns.bearerTokenHeader,
                        ApiFuzzContextTable.columns.bearerToken,
                        ApiFuzzContextTable.columns.apikeyHeader,
                        ApiFuzzContextTable.columns.apikey,
                        ApiFuzzContextTable.columns.hostname,
                        ApiFuzzContextTable.columns.port,
                        ApiFuzzContextTable.columns.fuzzcaseToExec,
                        ApiFuzzContextTable.columns.authnType,
                        
                        ApiFuzzCaseSetRunsTable.columns.Id.label("fuzzCaseSetRunsId"),
                        ApiFuzzCaseSetRunsTable.columns.startTime,
                        ApiFuzzCaseSetRunsTable.columns.endTime,
                        ApiFuzzCaseSetRunsTable.columns.status
                        
                    )
                    .join(ApiFuzzCaseSetRunsTable, ApiFuzzCaseSetRunsTable.columns.fuzzcontextId == ApiFuzzContextTable.columns.Id, isouter=True)
                    .all()
        )
        
        Session.commit()
        Session.close()
            
        
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
                fcView.apiDiscoveryMethod = rowDict['apiDiscoveryMethod']
                fcView.requestTextContent = rowDict['requestTextContent']
                fcView.requestTextFilePath = rowDict['requestTextFilePath']
                fcView.openapi3FilePath = rowDict['openapi3FilePath']
                fcView.openapi3Url = rowDict['openapi3Url']
                fcView.basicUsername = rowDict['basicUsername']
                fcView.basicPassword = rowDict['basicPassword'] 
                fcView.bearerTokenHeader = rowDict['bearerTokenHeader']
                fcView.bearerToken = rowDict['bearerToken']
                fcView.apikeyHeader = rowDict['apikeyHeader']
                fcView.apikey = rowDict['apikey']
                fcView.hostname = rowDict['hostname']
                fcView.port = rowDict['port']
                fcView.fuzzcaseToExec = rowDict['fuzzcaseToExec']
                fcView.authnType = rowDict['authnType']
                
                fcViews[fcid] = fcView
           
           fcsRunId = rowDict['fuzzCaseSetRunsId']
           #outer join causing "empty" records to also create, ignore empty FuzzCaseSetRun records
           if fcsRunId is not None:
                fcRunView = ApiFuzzCaseSetRunViewModel()
                fcRunView.fuzzCaseSetRunsId = fcsRunId
                fcRunView.fuzzcontextId = rowDict['fuzzcontextId']
                fcRunView.startTime = rowDict['startTime']
                fcRunView.endTime =  rowDict['endTime']
                fcRunView.status = rowDict['status']
                
                fcView = fcViews[fcRunView.fuzzcontextId]
                
                if fcView.fuzzCaseSetRuns is None:
                        fcView.fuzzCaseSetRuns = []
                        
                fcView.fuzzCaseSetRuns.append(fcRunView)
            
        fcList = []
        
        for x in fcViews.keys():
            fcList.append(fcViews[x])
        
        
        return True, '', fcList
        
    except Exception as e:
       eventstore.emitErr(e)
       return False, Utils.errAsText(e), []
    finally:
        Session.close()
        

def get_caseSets_with_runSummary(fuzzcontextId, fuzzCaseSetRunId):
    
    Session = scoped_session(session_factory)
    
    if fuzzCaseSetRunId == '':
        result = (
                        Session.query(ApiFuzzCaseSetTable, ApiFuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"),
                                ApiFuzzCaseSetTable.columns.fuzzcontextId.label("fuzzcontextId")
                                )
                        .filter(ApiFuzzCaseSetTable.c.fuzzcontextId == fuzzcontextId)
                        .all()
                     )
        
        Session.commit()
        Session.close()
        
    else:
        
        runSummaryQuery = (
                        Session.query(ApiFuzzRunSummaryPerCaseSetTable.columns.http2xx,
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.http3xx,
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.http4xx,
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.http5xx,
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.completedDataCaseRuns,
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.totalDataCaseRunsToComplete,
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.Id.label("runSummaryId"),
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.fuzzCaseSetId,
                                    ApiFuzzRunSummaryPerCaseSetTable.columns.fuzzCaseSetRunId
                                    )
                        .filter(ApiFuzzRunSummaryPerCaseSetTable.c.fuzzcontextId == fuzzcontextId,
                                ApiFuzzRunSummaryPerCaseSetTable.c.fuzzCaseSetRunId == fuzzCaseSetRunId)
                        .subquery()
                    )
        
        result = (
                        Session.query(
                                    ApiFuzzCaseSetTable, 
                                    ApiFuzzCaseSetTable.columns.Id.label("fuzzCaseSetId"),
                                    ApiFuzzCaseSetTable.columns.fuzzcontextId,
                                    runSummaryQuery.columns.runSummaryId,
                                    runSummaryQuery.columns.fuzzCaseSetRunId,
                                    runSummaryQuery.columns.http2xx,
                                    runSummaryQuery.columns.http3xx,
                                    runSummaryQuery.columns.http4xx,
                                    runSummaryQuery.columns.http5xx,
                                    runSummaryQuery.columns.completedDataCaseRuns,
                                    runSummaryQuery.columns.totalDataCaseRunsToComplete
                                )
                        .filter(ApiFuzzCaseSetTable.c.fuzzcontextId == fuzzcontextId)
                        .outerjoin(runSummaryQuery, runSummaryQuery.c.fuzzCaseSetId == ApiFuzzCaseSetTable.c.Id )
                        .all()
                     )
        
    Session.commit()
    Session.close()
    
    return result

def get_fuzz_request_response(fuzzCaseSetId, fuzzCaseSetRunId):
    
    Session = scoped_session(session_factory)
    
    rows = (Session.query(ApiFuzzDataCaseTable, ApiFuzzDataCaseTable.columns.Id.label("fuzzDataCaseId"),
                                ApiFuzzRequestTable.columns.Id.label('fuzzRequestId'),
                                ApiFuzzRequestTable.columns.datetime.label('requestDateTime'),
                                ApiFuzzRequestTable.columns.hostname,
                                ApiFuzzRequestTable.columns.port,
                                ApiFuzzRequestTable.columns.hostnamePort,
                                ApiFuzzRequestTable.columns.verb,
                                ApiFuzzRequestTable.columns.path,
                                ApiFuzzRequestTable.columns.querystring,
                                ApiFuzzRequestTable.columns.url,
                                ApiFuzzRequestTable.columns.headers,
                                ApiFuzzRequestTable.columns.contentLength,
                                ApiFuzzRequestTable.columns.invalidRequestError,
                                
                                ApiFuzzResponseTable.columns.Id.label('fuzzResponseId'),
                                ApiFuzzResponseTable.columns.datetime.label('responseDateTime'),
                                ApiFuzzResponseTable.columns.statusCode,
                                ApiFuzzResponseTable.columns.reasonPharse,
                                ApiFuzzResponseTable.columns.setcookieHeader,
                                ApiFuzzResponseTable.columns.headerJson,
                                ApiFuzzResponseTable.columns.contentLength
                                )
                    .filter(ApiFuzzDataCaseTable.c.fuzzCaseSetId == fuzzCaseSetId,
                            ApiFuzzDataCaseTable.c.fuzzCaseSetRunId == fuzzCaseSetRunId)
                    .join(ApiFuzzRequestTable, ApiFuzzRequestTable.columns.fuzzDataCaseId == ApiFuzzDataCaseTable.columns.Id, isouter=True)
                    .join(ApiFuzzResponseTable, ApiFuzzResponseTable.columns.fuzzDataCaseId == ApiFuzzDataCaseTable.columns.Id, isouter=True)
                    .all()
                )
    
    Session.commit()
    Session.close()
    
    return rows

def get_uploaded_files(requestId):
    
    Session = scoped_session(session_factory)
    
    rows = (Session
            .query(ApiFuzzRequestFileUploadTable.columns.Id,
                   ApiFuzzRequestFileUploadTable.columns.fileName)
            .filter(ApiFuzzRequestFileUploadTable.c.fuzzRequestId == requestId)
            .all())
    
    Session.commit()
    Session.close()
    
    return rows

def get_uploaded_file_content(fuzzRequestFileUploadId):
    Session = scoped_session(session_factory)
    
    row = (Session
            .query(ApiFuzzRequestFileUploadTable.columns.fileContent)
            .filter(ApiFuzzRequestFileUploadTable.c.Id == fuzzRequestFileUploadId)
            .first())
    
    Session.commit()
    Session.close()
    
    return row
    
    

def get_fuzz_request_response_messages(reqId, respId) -> tuple[str, str, str]:
    
    try:
        Session = scoped_session(session_factory)
    
        reqRow = (
                Session.query(
                    ApiFuzzRequestTable.columns.requestMessage,
                    ApiFuzzRequestTable.columns.verb,
                    ApiFuzzRequestTable.columns.path,
                    ApiFuzzRequestTable.columns.querystring,
                    ApiFuzzRequestTable.columns.url,
                    ApiFuzzRequestTable.columns.headers,
                    ApiFuzzRequestTable.columns.body,
                    ApiFuzzRequestTable.columns.invalidRequestError                  
                )
                .filter(ApiFuzzRequestTable.c.Id == reqId)
                .first()
                )
        
        Session.commit()
        Session.close()
        
        respRow = (
                Session.query(ApiFuzzResponseTable.columns.responseDisplayText,
                              ApiFuzzResponseTable.columns.body.label('responseBody'),
                              ApiFuzzResponseTable.columns.reasonPharse,
                              ApiFuzzResponseTable.columns.headerJson,
                              ApiFuzzResponseTable.columns.body
                )
                .filter(ApiFuzzResponseTable.c.Id == respId)
                .first()
                )
            
        Session.commit()
        Session.close()
        
        if reqRow is None or respRow is None:
            return {}, {}
        
        
        reqRowDict = reqRow._asdict()
        respRowDict = respRow._asdict()
        
        return (True, '', reqRowDict, respRowDict)
    
    except Exception as e:
        eventstore.emitErr(e)
        return (False, Utils.errAsText(e), {}, {})
        

def get_naughtypassword_by_id(id):
    
    Session = scoped_session(session_factory)
    
    row = Session.query(SeclistPasswordTable.columns.Content).filter(SeclistPasswordTable.c.id == id).one()
    
    Session.commit()
    Session.close()
        
    rowDict = row._asdict()
    
    return rowDict['Content']

def get_naughtypassword_row_count():
    Session = scoped_session(session_factory)
    
    count = Session.query(SeclistPasswordTable.c.id).count()
    
    Session.commit()
    Session.close()
    
    return count


def get_naughtyusername_by_id(id) -> str:
    
    Session = scoped_session(session_factory)
    
    row = Session.query(SeclistUsernameTable.columns.Content).filter(SeclistUsernameTable.c.id == id).one()
    
    Session.commit()
    Session.close()
        
    rowDict = row._asdict()
    
    return rowDict['Content']

def get_naughtyusername_row_count():
    
    Session = scoped_session(session_factory)
    
    count = Session.query(SeclistUsernameTable.c.id).count()
    
    Session.commit()
    Session.close()
    
    return count

def get_naughtystring_by_id(id) -> str:
    
    try:
        Session = scoped_session(session_factory)

        row = Session.query(SeclistBLNSTable.columns.Content).filter(SeclistBLNSTable.c.id == id).one()
        
        Session.commit()
        Session.close()
        
        rowDict = row._asdict()
        
        return rowDict['Content']
    
    except NoResultFound as e:
        print(e)
    

def get_naughtystring_row_count():
    Session = scoped_session(session_factory)
    
    count = Session.query(SeclistBLNSTable.c.id).count()
    
    Session.commit()
    Session.close()
    
    return count

def search_body(searchText: str, fuzzCaseSetId, fuzzCaseSetRunId):
    
    searchQuery = f'%{searchText}%'
    
    Session = scoped_session(session_factory)
    
    rows = (Session.query(ApiFuzzDataCaseTable, ApiFuzzDataCaseTable.columns.Id.label("fuzzDataCaseId"),
                                ApiFuzzRequestTable.columns.Id.label('fuzzRequestId'),
                                ApiFuzzRequestTable.columns.datetime.label('requestDateTime'),
                                ApiFuzzRequestTable.columns.hostname,
                                ApiFuzzRequestTable.columns.port,
                                ApiFuzzRequestTable.columns.hostnamePort,
                                ApiFuzzRequestTable.columns.verb,
                                ApiFuzzRequestTable.columns.path,
                                ApiFuzzRequestTable.columns.querystring,
                                ApiFuzzRequestTable.columns.url,
                                ApiFuzzRequestTable.columns.headers,
                                ApiFuzzRequestTable.columns.contentLength,
                                ApiFuzzRequestTable.columns.invalidRequestError,
                                ApiFuzzRequestTable.columns.body.label('requestBody'),
                                
                                ApiFuzzResponseTable.columns.Id.label('fuzzResponseId'),
                                ApiFuzzResponseTable.columns.datetime.label('responseDateTime'),
                                ApiFuzzResponseTable.columns.statusCode,
                                ApiFuzzResponseTable.columns.reasonPharse,
                                ApiFuzzResponseTable.columns.setcookieHeader,
                                ApiFuzzResponseTable.columns.headerJson,
                                ApiFuzzResponseTable.columns.contentLength,
                                ApiFuzzResponseTable.columns.body.label('responseBody')
                                )
                    .filter(ApiFuzzDataCaseTable.c.fuzzCaseSetId == fuzzCaseSetId,
                            ApiFuzzDataCaseTable.c.fuzzCaseSetRunId == fuzzCaseSetRunId
                    )
                    .join(ApiFuzzRequestTable, ApiFuzzRequestTable.columns.fuzzDataCaseId == ApiFuzzDataCaseTable.columns.Id, isouter=True)
                    .join(ApiFuzzResponseTable, ApiFuzzResponseTable.columns.fuzzDataCaseId == ApiFuzzDataCaseTable.columns.Id, isouter=True)
                    .all()
                )
    
    Session.commit()
    Session.close()
    
    return rows

def delete_api_fuzz_context(fuzzcontextId: str):
    
    uploadFileStmt = ApiFuzzRequestFileUploadTable.delete(ApiFuzzRequestFileUploadTable.c.fuzzcontextId == fuzzcontextId)
    apiRespStmt = ApiFuzzResponseTable.delete(ApiFuzzResponseTable.c.fuzzcontextId == fuzzcontextId)
    apiReqStmt = ApiFuzzRequestTable.delete(ApiFuzzRequestTable.c.fuzzcontextId == fuzzcontextId)
    apiDataCaseStmt = ApiFuzzDataCaseTable.delete(ApiFuzzDataCaseTable.c.fuzzcontextId == fuzzcontextId)
    runSumPerCaseSetStmt = ApiFuzzRunSummaryPerCaseSetTable.delete(ApiFuzzRunSummaryPerCaseSetTable.c.fuzzcontextId == fuzzcontextId)
    caseSetRunsStmt = ApiFuzzCaseSetRunsTable.delete(ApiFuzzCaseSetRunsTable.c.fuzzcontextId == fuzzcontextId)
    caseSetStmt =  ApiFuzzCaseSetTable.delete(ApiFuzzCaseSetTable.c.fuzzcontextId == fuzzcontextId)
    contextStmt = ApiFuzzContextTable.delete(ApiFuzzContextTable.c.Id == fuzzcontextId)
    
    Session = scoped_session(session_factory)
        
    Session.execute(apiRespStmt)
    
    Session.execute(apiReqStmt)
    
    Session.execute(apiDataCaseStmt)
    
    Session.execute(runSumPerCaseSetStmt)
    
    Session.execute(caseSetRunsStmt)
    
    Session.execute(caseSetStmt)
    
    Session.execute(contextStmt)
    
    Session.commit()
    
    Session.close()

def delete_api_fuzzCaseSetRun(fuzzCaseSetRunId: str):
    
    
    Session = scoped_session(session_factory)
    
    fuzzdatacaseIDs  = (
        Session.query(ApiFuzzDataCaseTable.columns.Id).
        filter(ApiFuzzDataCaseTable.columns.fuzzCaseSetRunId == fuzzCaseSetRunId)
    )
    
    fuzzrequestUploadFileTsql = (
        Session.query(ApiFuzzRequestFileUploadTable).
        filter(ApiFuzzRequestFileUploadTable.columns.fuzzDataCaseId.in_(fuzzdatacaseIDs.subquery()))
    )
    
    fuzzrequestUploadFileTsql.delete()
    
    fuzzrequestTsql = (
        Session.query(ApiFuzzRequestTable).
        filter(ApiFuzzRequestTable.columns.fuzzDataCaseId.in_(fuzzdatacaseIDs.subquery()))
    )
    
    fuzzrequestTsql.delete()
    
    fuzzresponseTsql = (
        Session.query(ApiFuzzResponseTable).
        filter(ApiFuzzResponseTable.columns.fuzzDataCaseId.in_(fuzzdatacaseIDs.subquery()))
    )

    fuzzresponseTsql.delete()
    
    apiDataCaseStmt = ApiFuzzDataCaseTable.delete(ApiFuzzDataCaseTable.c.fuzzCaseSetRunId == fuzzCaseSetRunId)
    
    runSumPerCaseSetStmt = ApiFuzzRunSummaryPerCaseSetTable.delete(ApiFuzzRunSummaryPerCaseSetTable.c.fuzzCaseSetRunId == fuzzCaseSetRunId)
    
    caseSetRunsStmt = ApiFuzzCaseSetRunsTable.delete(ApiFuzzCaseSetRunsTable.c.Id == fuzzCaseSetRunId)
    
    Session.execute(apiDataCaseStmt)
    
    Session.execute(runSumPerCaseSetStmt)
    
    Session.execute(caseSetRunsStmt)
    
    Session.commit()
    
    Session.close()

def save_updated_fuzzcasesets(fcsList: dict):
        
    Session = scoped_session(session_factory)
       
    stmt = (update(ApiFuzzCaseSetTable).
        where(ApiFuzzCaseSetTable.c.Id == bindparam('fuzzCaseSetId')).
        values(
                selected = bindparam('selected'),
                verb = bindparam('verb'),
                hostname =  bindparam('hostname'),
                port = bindparam('port'),
                path = bindparam('path'),
                querystringNonTemplate = bindparam('querystringNonTemplate'),
                bodyNonTemplate = bindparam('bodyNonTemplate'),
                headerNonTemplate = bindparam('headerNonTemplate'),
                file = bindparam('file'),
                fileDataTemplate = bindparam('fileDataTemplate'),
                pathDataTemplate = bindparam('pathDataTemplate'),
                querystringDataTemplate = bindparam('querystringDataTemplate'),
                bodyDataTemplate = bindparam('bodyDataTemplate'),
                headerDataTemplate = bindparam('headerDataTemplate'),
                requestMessage = bindparam('requestMessage')
            )
    )
    
    Session.execute(stmt, fcsList)
    
    Session.commit()
        
    Session.close()
    
    return (True, '')

def update_api_fuzz_context(fuzzcontext: ApiFuzzContextUpdate):
    
    stmt = (
            update(ApiFuzzContextTable).
            where(ApiFuzzContextTable.c.Id == fuzzcontext.fuzzcontextId).
            values(
                    name = fuzzcontext.name,
                    basicUsername = fuzzcontext.basicUsername,
                    basicPassword = fuzzcontext.basicPassword,
                    bearerTokenHeader = fuzzcontext.bearerTokenHeader,
                    bearerToken = fuzzcontext.bearerToken,
                    apikeyHeader = fuzzcontext.apikeyHeader,
                    apikey = fuzzcontext.apikey,
                    hostname = fuzzcontext.hostname,
                    port = fuzzcontext.port,
                    fuzzcaseToExec = fuzzcontext.fuzzcaseToExec,
                    authnType = fuzzcontext.authnType
                   )
            )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()

def update_rqmsg_in_fuzz_context(rqMsg: str, fuzzcontextId):
    
    stmt = (
            update(ApiFuzzContextTable).
            where(ApiFuzzContextTable.c.Id == fuzzcontextId).
            values(
                    requestTextContent = rqMsg
                   )
            )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()

# mutations
def insert_db_fuzzcontext(fuzzcontext: ApiFuzzContext):

        Session = scoped_session(session_factory)
        
        fuzzcontextStmt = (
            insert(ApiFuzzContextTable).
            values(
                   Id=fuzzcontext.Id, 
                   datetime= datetime.now(),
                   apiDiscoveryMethod = fuzzcontext.apiDiscoveryMethod,
                   name = fuzzcontext.name,
                    hostname = fuzzcontext.hostname,
                    port = fuzzcontext.port,
                    fuzzcaseToExec = fuzzcontext.fuzzcaseToExec,
                    requestTextContent = fuzzcontext.requestTextContent,
                    requestTextFilePath = fuzzcontext.requestTextFilePath,
                    openapi3FilePath = fuzzcontext.openapi3FilePath,
                    openapi3Url = fuzzcontext.openapi3Url,
                    authnType = fuzzcontext.authnType,
                    basicUsername = fuzzcontext.basicUsername,
                    basicPassword = fuzzcontext.basicPassword,
                    bearerTokenHeader = fuzzcontext.bearerTokenHeader,
                    bearerToken = fuzzcontext.bearerToken,
                    apikeyHeader = fuzzcontext.apikeyHeader,
                    apikey = fuzzcontext.apikey
                   )
         )
        
        Session.execute(fuzzcontextStmt)
        
        # insert fuzzcasesets
        if len(fuzzcontext.fuzzcaseSets) > 0:
            for fcset in fuzzcontext.fuzzcaseSets:
                
                fileType= ''
                if fcset.file != '':
                    fileType = fcset.file.filename
                
                fcSetStmt = (
                    insert(ApiFuzzCaseSetTable).
                    values(
                        Id=fcset.Id, 
                        selected = fcset.selected,
                        verb = fcset.verb,
                        hostname = fcset.hostname,
                        port = fcset.port,
                        path = fcset.path,
                        querystringNonTemplate = fcset.querystringNonTemplate,
                        bodyNonTemplate = fcset.bodyNonTemplate,
                        pathDataTemplate = fcset.pathDataTemplate,
                        querystringDataTemplate = fcset.querystringDataTemplate,
                        headerDataTemplate = fcset.headerDataTemplate,
                        headerNonTemplate = fcset.headerNonTemplate,
                        bodyDataTemplate =  fcset.bodyDataTemplate,
                        file = fileType,
                        fileDataTemplate = fcset.fileDataTemplate,
                        fuzzcontextId = fuzzcontext.Id,
                        requestMessage = fcset.requestMessage
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
    

def insert_api_fuzzrequest_fileupload(Id, wordlist_type, fileName,fileContent, fuzzRequestId, fuzzDataCaseId, fuzzcontextId) -> None:
    stmt = (
            insert(ApiFuzzRequestFileUploadTable).
            values(
                    Id=Id,
                    datetime = datetime.now(),
                    wordlist_type = wordlist_type,
                    fileName = fileName,
                    fileContent = fileContent,
                    fuzzRequestId = fuzzRequestId,
                    fuzzDataCaseId = fuzzDataCaseId,
                    fuzzcontextId = fuzzcontextId
                   )
         )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
    
def update_api_fuzzCaseSetRun_status(fuzzCaseSetRunId, status = 'completed', message='') -> None:
    stmt = (
            update(ApiFuzzCaseSetRunsTable).
            where(ApiFuzzCaseSetRunsTable.c.Id == fuzzCaseSetRunId).
            values(
                    endTime = datetime.now(),
                    status = status,
                    message = message
                   )
            )
    
    Session = scoped_session(session_factory)
        
    Session.execute(stmt)
    
    Session.commit()
    Session.close()
                
def insert_api_fuzzdatacase(fuzzCaseSetRunId, fdc: ApiFuzzDataCase) -> None:
    
    Session = scoped_session(session_factory)
    
    stmt = (
            insert(ApiFuzzDataCaseTable).
            values(
                    Id = fdc.Id,
                    fuzzCaseSetRunId = fuzzCaseSetRunId,
                    fuzzCaseSetId = fdc.fuzzCaseSetId,
                    fuzzcontextId = fdc.fuzzcontextId
                   )
         )
    
    requestStmt = (
                insert(ApiFuzzRequestTable).
                values(
                        Id = fdc.request.Id,
                        datetime = fdc.request.datetime,
                        fuzzDataCaseId = fdc.request.fuzzDataCaseId,
                        fuzzcontextId = fdc.request.fuzzcontextId,
                        hostname = fdc.request.hostname,
                        port = fdc.request.port,
                        hostnamePort = fdc.request.hostnamePort,
                        verb = fdc.request.verb,
                        path = fdc.request.path,
                        querystring = fdc.request.querystring,
                        url = fdc.request.url,
                        headers = fdc.request.headers,
                        body = fdc.request.body,
                        invalidRequestError = fdc.request.invalidRequestError,
                        requestMessage = fdc.request.requestMessage,
                        contentLength = fdc.request.contentLength
                    )
            )
    
    responseStmt = (
            insert(ApiFuzzResponseTable).
            values(
                    Id = fdc.response.Id,
                    datetime = fdc.response.datetime,
                    fuzzDataCaseId = fdc.response.fuzzDataCaseId,
                    fuzzcontextId = fdc.response.fuzzcontextId,
                    statusCode = fdc.response.statusCode,
                    reasonPharse = fdc.response.reasonPharse,
                    responseDisplayText = fdc.response.responseDisplayText,
                    setcookieHeader = fdc.response.setcookieHeader,
                    headerJson = fdc.response.headerJson,
                    body = fdc.response.body,
                    contentLength = fdc.response.contentLength
                   )
         )
    
    
        
    Session.execute(stmt)
    Session.execute(requestStmt)
    Session.execute(responseStmt)
    
    Session.commit()
    Session.close()
        
    # Session.close_all()
    
def insert_api_fuzzrequest(fr: ApiFuzzRequest) -> None:
    
    try:
        if fr.Id is None:
            raise Exception('ApiFuzzRequest is None while persisting')
                        
        stmt = (
                insert(ApiFuzzRequestTable).
                values(
                        Id = fr.Id,
                        datetime = fr.datetime,
                        fuzzDataCaseId = fr.fuzzDataCaseId,
                        fuzzcontextId = fr.fuzzcontextId,
                        hostname = fr.hostname,
                        port = fr.port,
                        hostnamePort = fr.hostnamePort,
                        verb = fr.verb,
                        path = fr.path,
                        querystring = fr.querystring,
                        url = fr.url,
                        headers = fr.headers,
                        body = fr.body,
                        invalidRequestError = fr.invalidRequestError,
                        requestMessage = fr.requestMessage,
                        contentLength = fr.contentLength
                    )
            )
        
        Session = scoped_session(session_factory)
            
        Session.execute(stmt)
        
        # Session.close_all()
        
        Session.commit()
        Session.close()
        
    except Exception as e:
        eventstore.emitErr(e)
    
    
    
    
def insert_api_fuzzresponse(fr: ApiFuzzResponse) -> None:
    
    try:
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
                    contentLength = fr.contentLength
                   )
         )

        Session = scoped_session(session_factory)
            
        Session.execute(stmt)
        
        Session.commit()
        Session.close()
        
    except Exception as e:
        eventstore.emitErr(e)
    

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
    fuzzcontext.apiDiscoveryMethod = rowDict['apiDiscoveryMethod']
    fuzzcontext.name = rowDict['name']
    fuzzcontext.hostname = rowDict['hostname']
    fuzzcontext.port = rowDict['port']
    fuzzcontext.fuzzcaseToExec = rowDict['fuzzcaseToExec']
    fuzzcontext.requestTextContent = rowDict['requestTextContent']
    fuzzcontext.requestTextFilePath = rowDict['requestTextFilePath']
    fuzzcontext.openapi3FilePath = rowDict['openapi3FilePath']
    fuzzcontext.openapi3Url = rowDict['openapi3Url']
    fuzzcontext.authnType = rowDict['authnType']
    fuzzcontext.basicUsername = rowDict['basicUsername']
    fuzzcontext.basicPassword = rowDict['basicPassword']
    fuzzcontext.bearerTokenHeader = rowDict['bearerTokenHeader']
    fuzzcontext.bearerToken = rowDict['bearerToken']
    fuzzcontext.apikeyHeader = rowDict['apikeyHeader']
    fuzzcontext.apikey = rowDict['apikey']
    
    return fuzzcontext
    

def create_fuzzcaseset_from_dict(rowDict):
    fcs = ApiFuzzCaseSet()
    fcs.Id = rowDict['fuzzCaseSetId']
    fcs.hostname = rowDict['hostname']
    fcs.port = rowDict['port']
    fcs.path = rowDict['path']
    fcs.pathDataTemplate = rowDict['pathDataTemplate']
    fcs.querystringDataTemplate= rowDict['querystringDataTemplate']
    fcs.bodyDataTemplate= rowDict['bodyDataTemplate']
    fcs.headerDataTemplate = rowDict['headerDataTemplate']
    fcs.querystringNonTemplate = rowDict['querystringNonTemplate']
    fcs.bodyNonTemplate = rowDict['bodyNonTemplate']
    fcs.selected = rowDict['selected']
    fcs.verb = rowDict['verb']
    
    fcs.file = rowDict['file']
    fcs.fileDataTemplate = rowDict['fileDataTemplate']

    return fcs



def create_runsummary_per_fuzzcaseset(Id, fuzzCaseSetId, fuzzCaseSetRunId, fuzzcontextId, totalRunsToComplete=1):
    
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
    
def update_casesetrun_summary(fuzzcontextId, fuzzCaseSetRunId, fuzzCaseSetId,  caseSetRunSummaryId, httpCode, completedDataCaseRuns = 0) -> ApiFuzzCaseSets_With_RunSummary_ViewModel :
    
    Session = scoped_session(session_factory)

    summary = (
                Session
                .query(ApiFuzzRunSummaryPerCaseSetTable)
                .filter(ApiFuzzRunSummaryPerCaseSetTable.c.Id == caseSetRunSummaryId)
                .first()
               )
    rowDict =  summary._asdict()
    existingHttp2xx = rowDict['http2xx']
    existingHttp3xx = rowDict['http3xx']
    existingHttp4xx = rowDict['http4xx']
    existingHttp5xx = rowDict['http5xx']
    existingCompletedDataCaseRuns = rowDict['completedDataCaseRuns']
    totalDataCaseRunsToComplete = rowDict['totalDataCaseRunsToComplete']
    
    if httpCode >= 200 and httpCode <= 299:
        existingHttp2xx = existingHttp2xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == caseSetRunSummaryId).
            values(
                    http2xx = existingHttp2xx
                   )
            )
        Session.execute(stmt)
        Session.commit()
        Session.close()
    
    elif httpCode >= 300 and httpCode <= 399:
        existingHttp3xx = existingHttp3xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == caseSetRunSummaryId).
            values(
                    http3xx = existingHttp3xx
                   )
            )
        Session.execute(stmt)
        Session.commit()
        Session.close()
    
    elif httpCode >= 400 and httpCode <= 499:
        existingHttp4xx = existingHttp4xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == caseSetRunSummaryId).
            values(
                    http4xx = existingHttp4xx
                   )
            )
        Session.execute(stmt)
        Session.commit()
        Session.close()
        
    elif httpCode >= 500 and httpCode <= 599:
        existingHttp5xx = existingHttp5xx + 1
        stmt = (
            update(ApiFuzzRunSummaryPerCaseSetTable).
            where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == caseSetRunSummaryId).
            values(
                    http5xx = existingHttp5xx
                   )
            )
        Session.execute(stmt)
        Session.commit()
        Session.close()
        
    # +1 to completed run
    existingCompletedDataCaseRuns = existingCompletedDataCaseRuns + completedDataCaseRuns
    stmt = (
        update(ApiFuzzRunSummaryPerCaseSetTable).
        where(ApiFuzzRunSummaryPerCaseSetTable.c.Id == caseSetRunSummaryId).
        values(
                completedDataCaseRuns = existingCompletedDataCaseRuns
                )
        )
    Session.execute(stmt)
    Session.commit()
    Session.close()


def get_fuzzcaseset_run_statistics(caseSetRunSummaryId, fuzzCaseSetId, fuzzCaseSetRunId, fuzzcontextId):
    
    Session = scoped_session(session_factory)
    
    latestSummary = (
                Session
                .query(ApiFuzzRunSummaryPerCaseSetTable)
                .filter(ApiFuzzRunSummaryPerCaseSetTable.c.Id == caseSetRunSummaryId)
                .first()
               )
    rowDict =  latestSummary._asdict()
    existingHttp2xx = rowDict['http2xx']
    existingHttp3xx = rowDict['http3xx']
    existingHttp4xx = rowDict['http4xx']
    existingHttp5xx = rowDict['http5xx']
    existingCompletedDataCaseRuns = rowDict['completedDataCaseRuns']
    totalDataCaseRunsToComplete = rowDict['totalDataCaseRunsToComplete']
    
    # retrieve again from DB to get the latest stats as during the above code execution, concurrent fuzzing process
    # will be updating DB at the same time, so once execution reach this line of code, stats could be likely outdated.
    # therefore retrieving again is necessary
    summary = ApiFuzzCaseSets_With_RunSummary_ViewModel()
    summary.Id = caseSetRunSummaryId
    summary.fuzzCaseSetId = fuzzCaseSetId
    summary.fuzzCaseSetRunId = fuzzCaseSetRunId
    summary.fuzzcontextId = fuzzcontextId
    summary.http2xx = existingHttp2xx
    summary.http3xx = existingHttp3xx
    summary.http4xx = existingHttp4xx
    summary.http5xx = existingHttp5xx
    summary.completedDataCaseRuns = existingCompletedDataCaseRuns
    summary.totalDataCaseRunsToComplete = totalDataCaseRunsToComplete
    return summary      
               
    
# create tables if not exist
metadata.create_all()


