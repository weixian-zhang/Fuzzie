
export class ApiFuzzcontextRuns {
   
    public fuzzCaseSetRunsId  = '';
     
    public fuzzcontextId  = '';
     
    public startTime;
     
    public endTime;
     
    public status  = '';
}

export class ApiFuzzContextUpdate {
    public fuzzcontextId: string;
    public name: string;
    public basicUsername: string;
    public basicPassword: string;
    public bearerTokenHeader: string;
    public bearerToken: string;
    public apikeyHeader: string;
    public apikey: string;
    public fuzzcaseToExec: number;
    public authnType: string;
    public templateVariables: string;

}

export class ApiFuzzContext {
     
    public Id = '';
    public name ='my REST Api';
    public datetime ='';
    public requestTextContent ='';
    public requestTextFilePath ='';
    public openapi3FilePath ='';
    public openapi3Url ='';
    public openapi3Content ='';
    public authnType ='Anonymous';
    public basicUsername ='';
    public basicPassword ='';
    public bearerTokenHeader ='Authorization';
    public bearerToken ='';
    public apikeyHeader ='Authorization';
    public apikey ='';
    public fuzzcaseToExec =500;
    public templateVariables ='';

    fuzzCaseSetRuns: Array<ApiFuzzcontextRuns> = []
}

export class ApiFuzzCaseSetsWithRunSummariesFuzzContext {
    public fuzzcontextId = ''
    public templateVariables = ''
    public fcsRunSums: Array<ApiFuzzCaseSetsWithRunSummaries> = []
}

export class ApiFuzzCaseSetsWithRunSummaries {
    public fuzzCaseSetId = '';
    public fuzzCaseSetRunId = '';
    public fuzzcontextId = '';
    public selected = true;
    public verb = '';
    public urlNonTemplate = '';
    public urlDataTemplate = '';
    public bodyNonTemplate = '';
    public headerNonTemplate = '';
    public authnType = '';
    public requestMessage = '';
    public runSummaryId = '';
    public http2xx = 0;
    public http3xx = 0;
    public http4xx = 0;
    public http5xx = 0;
    public completedDataCaseRuns = 0; 
    public totalDataCaseRunsToComplete = 0;
    public isGraphQL = false;
    public graphQLVariableNonTemplate = ''
    public graphQLVariableDataTemplate = ''
    public templateVariables = ''
    public fileNonTemplate = ''
    public fileDataTemplate = ''
}


export class FuzzResponse {
    public Id = '';
    public responseDateTime;
    public statusCode = '';
    public reasonPharse = '';
    public headerJson = '';
    public setcookieHeader = '';
    public body = '';
    public contentLength = 0;
    public responseDisplayText = ''
}


export class FuzzDataCase {
    public fuzzDataCaseId = '';
    public fuzzCaseSetId = '';
    public request: FuzzRequest;
    public response: FuzzResponse;
}

export class WebApiFuzzerInfo {
    public isFuzzing = false;
    public fuzzContextId = '';
    public fuzzCaseSetRunId = '';
}

export class FuzzerStatus {
    public timestamp;
    public alive = false
    public isDataLoaded = false
    public message =''
    public webapiFuzzerInfo: WebApiFuzzerInfo;
}


export class FuzzRequest {
    public Id = ''
    public requestDateTime;
    public hostname = '';
    public port = 443
    public verb = '';
    public url = '';
    public path = '';
    public querystring = '';
    public headers = '';
    public body = '';
    public contentLength = 0
    public requestMessage = '';
    public invalidRequestError = '';
    public uploadFileName = ''
}

export class FuzzResponse_ViewModel {
    public Id = '';
    public responseDateTime;
    public statusCode = '';
    public reasonPharse = '';
    public headerJson = '';
    public setcookieHeader = '';
    public body = '';
    public contentLength = 0;
    public responseDisplayText = '';
}
    
export class FuzzDataCase_ViewModel {
    public fuzzDataCaseId = '';
    public fuzzCaseSetId = '';
    public request: FuzzRequest;
    public response: FuzzResponse;

}


export class FuzzRequestFileUpload_ViewModel {
    public Id = '';
    public fileName = '';
}
    
export class FuzzRequestFileUploadQueryResult {
    public ok = '';
    public error = '';
    public result: Array<FuzzRequestFileUpload_ViewModel|any>;
}


export class FuzzRequestResponseMessage_ViewModel {
    ok = false;
    error = '';
    requestVerb = '';
    requestMessage = '';
    requestPath = '';
    requestQuerystring = '';
    requestHeader = '';
    requestBody = '';
    
    responseDisplayText = '';
    responseReasonPhrase = '';
    responseHeader = '';
    responseBody= '';
}
    

export class FuzzRequestResponseMessage_QueryResult {
    ok = false;
    error = '';
    result : FuzzRequestResponseMessage_ViewModel;
}
