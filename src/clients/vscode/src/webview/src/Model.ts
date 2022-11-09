

export class ApiFuzzcontextRuns {
     
    public fuzzCaseSetRunsId  = '';
     
    public fuzzcontextId  = '';
     
    public startTime;
     
    public endTime;
     
    public status  = '';
}

export class FuzzContext {
     
    public Id = '';
     
    public datetime;
     
    public name = '';
     
    public requestMessageText = '';
     
    public requestMessageFilePath  = '';
     
    public openapi3FilePath  = '';
     
    public openapi3Url  = '';
     
    public hostname  = '';
     
    public port = 0;
     
    public fuzzMode  = '';
     
    public fuzzcaseToExec = 100;
     
    public authnType  = '';

    fuzzCaseSetRuns: Array<ApiFuzzcontextRuns> = []
}

