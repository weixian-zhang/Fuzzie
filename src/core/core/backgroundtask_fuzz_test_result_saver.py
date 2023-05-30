import threading
import time
from fuzz_test_result_queue import FuzzTestResultQueue
from models.webapi_fuzzcontext import FuzzTestResult, WordlistType
from graphql_models import ApiFuzzCaseSets_With_RunSummary_ViewModel
from eventstore import EventStore
import shortuuid
from db import insert_api_fuzzdatacase, update_casesetrun_summary, insert_api_fuzzrequest_fileupload
import io
eventstore = EventStore()
from utils import Utils
import base64

class BackgroundTask_FuzzTest_Result_Saver(threading.Thread):
    
    def run(self,*args,**kwargs):
        while True:
            try:
                
                if len(FuzzTestResultQueue.resultQueue) > 0:
                    
                    try:
                        ftResult: FuzzTestResult = FuzzTestResultQueue.resultQueue.pop()

                        insert_api_fuzzdatacase(ftResult.fuzzCaseSetRunId, ftResult.fuzzDataCase)
                        
                        runSummaryPerCaseSetDict = update_casesetrun_summary(fuzzcontextId = ftResult.fuzzcontextId,
                                                    fuzzCaseSetRunId = ftResult.fuzzCaseSetRunId, 
                                                    fuzzCaseSetId=ftResult.fuzzCaseSetId,
                                                    completedDataCaseRuns=ftResult.completedDataCaseRuns,
                                                    httpCode=ftResult.httpCode,
                                                    caseSetRunSummaryId=ftResult.caseSetRunSummaryId)
                    
                    
                        # save file content
                        if Utils.isNoneEmpty(ftResult.file) == False:
                            
                            try:
                            
                                wordlist_type = ftResult.file.wordlist_type
                                filename = ftResult.file.filename
                                content = ''
                                
                                if wordlist_type == WordlistType.image:
                                    ftResult.file.content.seek(0)
                                    byteVal = ftResult.file.content.getvalue()
                                    decoded = Utils.try_decode_bytes_string(byteVal)
                                    content = decoded
                                else:
                                    if not isinstance(ftResult.file.content, str):
                                        content = Utils.try_decode_bytes_string(ftResult.file.content)
                                    else:
                                        content = ftResult.file.content
                                    
                                insert_api_fuzzrequest_fileupload(
                                    Id=shortuuid.uuid(),
                                    wordlist_type=wordlist_type,
                                    fileName=filename,
                                    fileContent=content,
                                    fuzzcontextId=ftResult.fuzzcontextId,
                                    fuzzDataCaseId=ftResult.fuzzDataCase.Id,
                                    fuzzRequestId=ftResult.fuzzDataCase.request.Id
                                    )
                                
                            except Exception as e:
                                eventstore.emitErr(e, 'BackgroundTask_FuzzTest_Result_Saver')
                                continue
                    
                        # send stats over websocket to webview
                        fcsRunSummary = self.create_runSummary_Stats(
                            caseSetRunSummaryId=ftResult.caseSetRunSummaryId,
                            fuzzCaseSetId=ftResult.fuzzCaseSetId,
                            fuzzCaseSetRunId=ftResult.fuzzCaseSetRunId,
                            fuzzcontextId=ftResult.fuzzcontextId,
                            runSumStatsDict=runSummaryPerCaseSetDict
                            )
                        
                        eventstore.feedback_client('fuzz.update.casesetrunsummary', fcsRunSummary)
                    
                    
                    except Exception as e:
                        eventstore.emitErr(e, 'BackgroundTask_FuzzTest_Result_Saver')
                        continue
                            
                else:
                    time.sleep(1)
                
            except Exception as e:
                eventstore.emitErr(e, 'BackgroundTask_FuzzTest_Result_Saver')
                continue
            

    def create_runSummary_Stats(self, caseSetRunSummaryId, fuzzCaseSetId, fuzzCaseSetRunId, fuzzcontextId, runSumStatsDict) -> ApiFuzzCaseSets_With_RunSummary_ViewModel:
        summary = ApiFuzzCaseSets_With_RunSummary_ViewModel()
        summary.Id = caseSetRunSummaryId
        summary.fuzzCaseSetId = fuzzCaseSetId
        summary.fuzzCaseSetRunId = fuzzCaseSetRunId
        summary.fuzzcontextId = fuzzcontextId
        summary.http2xx = runSumStatsDict['http2xx'] if 'http2xx' in runSumStatsDict else 0
        summary.http3xx = runSumStatsDict['http3xx'] if 'http3xx' in runSumStatsDict else 0
        summary.http4xx = runSumStatsDict['http4xx'] if 'http4xx' in runSumStatsDict else 0
        summary.http5xx = runSumStatsDict['http5xx'] if 'http5xx' in runSumStatsDict else 0
        summary.completedDataCaseRuns = runSumStatsDict['completedDataCaseRuns'] if 'completedDataCaseRuns' in runSumStatsDict else 0
        summary.totalDataCaseRunsToComplete = runSumStatsDict['totalDataCaseRunsToComplete'] if 'totalDataCaseRunsToComplete' in runSumStatsDict else 0
        
        return summary
            

