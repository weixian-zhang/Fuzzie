import threading
import time
import asyncio
from fuzz_test_result_queue import FuzzTestResultQueue
from models.webapi_fuzzcontext import FuzzTestResult
from eventstore import EventStore
import shortuuid
from db import insert_api_fuzzdatacase, update_casesetrun_summary, insert_api_fuzzrequest_fileupload
eventstore = EventStore()

class BackgroundTask_FuzzTest_Result_Saver(threading.Thread):
    
    
    def run(self,*args,**kwargs):
        while True:
            try:
                
                if len(FuzzTestResultQueue.resultQueue) > 0:
                    
                    ftResult: FuzzTestResult = FuzzTestResultQueue.resultQueue.pop()

                    insert_api_fuzzdatacase(ftResult.fuzzCaseSetRunId, ftResult.fuzzDataCase)
                    
                    update_casesetrun_summary(fuzzcontextId = ftResult.fuzzcontextId,
                                              fuzzCaseSetRunId = ftResult.fuzzCaseSetRunId, 
                                              fuzzCaseSetId=ftResult.fuzzCaseSetId,
                                              completedDataCaseRuns=ftResult.completedDataCaseRuns,
                                              httpCode=ftResult.httpCode,
                                              caseSetRunSummaryId=ftResult.caseSetRunSummaryId)
                    
                    # save file content
                    if ftResult.file != '':
                        for ftuple in ftResult.files:
                            wordlist_type, fileName, content = ftuple
                            insert_api_fuzzrequest_fileupload(
                                Id=shortuuid.uuid(),
                                wordlist_type=wordlist_type,
                                fileName=fileName,
                                fileContent=content,
                                fuzzcontextId=ftResult.fuzzcontextId,
                                fuzzDataCaseId=ftResult.fuzzDataCase.Id,
                                fuzzRequestId=ftResult.fuzzDataCase.request.Id
                            )
                   
                    
                else:
                    time.sleep(1)
                
                            
            except Exception as e:
                eventstore.emitErr(e, 'BackgroundTask_FuzzTest_Result_Saver')
                continue
            

