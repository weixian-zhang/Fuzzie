
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