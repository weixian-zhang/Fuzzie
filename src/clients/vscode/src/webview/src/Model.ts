
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
    public hostname: string;
    public port: number;
    public fuzzcaseToExec: number;
    public authnType: string;
}

export class ApiFuzzContext {
     
    public Id = '';
    public name ='my REST Api';
    public datetime ='';
    public apiDiscoveryMethod  ='';
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
    public hostname ='httpbin.org';
    public port = 443;
    public fuzzcaseToExec =100;

    fuzzCaseSetRuns: Array<ApiFuzzcontextRuns> = []
}

