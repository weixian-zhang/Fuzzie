import threading
import time
from fuzz_test_result_queue import FuzzTestResultQueue
from models.webapi_fuzzcontext import FuzzTestResult, WordlistType
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
                    
                    ftResult: FuzzTestResult = FuzzTestResultQueue.resultQueue.pop()

                    insert_api_fuzzdatacase(ftResult.fuzzCaseSetRunId, ftResult.fuzzDataCase)
                    
                    update_casesetrun_summary(fuzzcontextId = ftResult.fuzzcontextId,
                                              fuzzCaseSetRunId = ftResult.fuzzCaseSetRunId, 
                                              fuzzCaseSetId=ftResult.fuzzCaseSetId,
                                              completedDataCaseRuns=ftResult.completedDataCaseRuns,
                                              httpCode=ftResult.httpCode,
                                              caseSetRunSummaryId=ftResult.caseSetRunSummaryId)
                    
                    # save file content
                    if not Utils.isNoneEmpty(ftResult.file):
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
                            
                   
                    
                else:
                    time.sleep(1)
                
                            
            except Exception as e:
                eventstore.emitErr(e, 'BackgroundTask_FuzzTest_Result_Saver')
                continue
            

