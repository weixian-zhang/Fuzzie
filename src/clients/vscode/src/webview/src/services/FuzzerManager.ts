
import FuzzerWebClient from "./FuzzerWebClient";
import { 
    ApiFuzzContext, ApiFuzzcontextRuns, ApiFuzzContextUpdate, 
    ApiFuzzCaseSetsWithRunSummaries, FuzzDataCase, FuzzerStatus
}
from "../Model";

export default class FuzzerManager
{
    private _wc: FuzzerWebClient;
    private isFuzzerWSConnected = false;
    private isFuzzerGraphQLRunning = true;
    
    public constructor(wc: FuzzerWebClient)
    {
        this._wc = wc;
    }

    

    public async fuzz(fuzzContextId: string): Promise<[boolean, string]> {
        const query = `
        mutation fuzz {
            fuzz(fuzzcontextId:"${fuzzContextId}") {
                  ok,
                  msg
            }
          }
        `;

        try {
            const [ok, msg] = await this._wc.graphql(query)

            return [ok, msg];
            
        } catch (error: any) {
            return [false, error.message];
        }
    }

    public async httpGetOpenApi3FromUrl(url: string): Promise<[boolean, string, string]> {

        const [ok, error, spec] = await this._wc.httpGetString(url)

        return [ok, error, spec];
    }

    public async getApiFuzzCaseSetsWithRunSummaries(fuzzcontextId: string, fuzzCaseSetRunId: string): Promise<[boolean, string, [ApiFuzzCaseSetsWithRunSummaries|null]]> {
        
        const query = `
            query {
                fuzzCaseSetWithRunSummary(
                        fuzzcontextId: "${fuzzcontextId}",
                        fuzzCaseSetRunId: "${fuzzCaseSetRunId}") {
                    ok,
                    error,
                    result {
                        fuzzCaseSetId
                        fuzzCaseSetRunId
                        fuzzcontextId
                        selected 
                        verb
                        path
                        querystringNonTemplate
                        bodyNonTemplate
                        headerNonTemplate
                        authnType
                        runSummaryId
                        http2xx
                        http3xx
                        http4xx
                        http5xx
                        completedDataCaseRuns
                        totalDataCaseRunsToComplete
                        file
                    }
                }
            }
        `;

        const [ok, err, resp] = await this._wc.graphql(query)

        if(!ok)
        {
            return [ok, err, [null]];
        }

        const gqlOK = ok;
        const error = err;
        const result = resp?.data.data.fuzzCaseSetWithRunSummary.result;

        return [gqlOK, error, result];
    }

    public async saveFuzzCaseSetSelected(fcsList): Promise<[boolean, string]> {

        let fcsStr = JSON.stringify(fcsList);

        fcsStr = fcsStr.replaceAll("\"fuzzCaseSetId\"","fuzzCaseSetId");

        fcsStr = fcsStr.replaceAll("\"selected\"","selected");

        const query = `
        mutation update_fuzzcaseset_selected {
            saveApiFuzzcasesetSelected(fcsus: ${fcsStr})
                 {
                     ok,
                     error
                 }
         }
        `

        const [ok, err, resp] = await this._wc.graphql(query)

        if(!ok)
        {
            return [ok, err];
        }

        const gqlOK = resp?.data.data.saveApiFuzzcasesetSelected.ok;
        const error = resp?.data.data.saveApiFuzzcasesetSelected.error;

        return [gqlOK, error];
    }

    public async deleteApiFuzzContext(fuzzcontextId): Promise<[boolean, string]> {
        const query = `
            mutation delete {
                deleteApiFuzzContext(fuzzcontextId:"${fuzzcontextId}"){
                ok
                error
                }
            }
        `

        const [ok, err, resp] = await this._wc.graphql(query)

        if(!ok)
        {
            return [ok, err];
        }

        const gqlOK = resp?.data.data.deleteApiFuzzContext.ok;
        const error = resp?.data.data.deleteApiFuzzContext.error;

        return [gqlOK, error];
    }

    // public async updateApiFuzzContext(fuzzcontext: ApiFuzzContextUpdate): Promise<[boolean, string]>
    // {
    //     const [ok, error] = await this._wc.updateApiFuzzContext(fuzzcontext);

    //     return [ok, error];
    // }

    public async newFuzzContext(fuzzcontext: ApiFuzzContext): Promise<ApiFuzzContext>
    {
        
        const result = await this._wc.createNewApiFuzzContext(fuzzcontext);

        return result;
    }

    public async getFuzzcontexts(): Promise<[boolean, string, Array<ApiFuzzContext>]>
    {
        const [ok, err, data] = await this._wc.getFuzzContexts()

        if(!ok || data == undefined)
            return [ok, err, []];

        const fcs: Array<ApiFuzzContext> = [];

        data.forEach(fc => {
            
            const newFC = new ApiFuzzContext();

            this.propMap(fc, newFC);

            fcs.push(newFC);

            if(fc.fuzzCaseSetRuns != undefined)
            {
                fc.fuzzCaseSetRuns.forEach(ele => {

                    const fcRun = new ApiFuzzcontextRuns();

                    this.propMap(ele, fcRun);

                    newFC.fuzzCaseSetRuns.push(fcRun);

                });
            }
        });

        return [true, '', fcs];
    }

    public async getFuzzRequestResponse(fuzzCaseSetId: string, fuzzCaseSetRunId: string): Promise<[boolean, string, Array<FuzzDataCase>]> {
        const query = `
        query {
            fuzzRequestResponse(
                fuzzCaseSetId: "${fuzzCaseSetId}",
                fuzzCaseSetRunId: "${fuzzCaseSetRunId}") {
                ok,
                error,
                result {
                    fuzzDataCaseId
                    fuzzCaseSetId
                    request {
                        Id
                        requestDateTime
                        hostname
                        port
                        verb
                        path
                        querystring
                        url
                        headers
                        body
                        contentLength
                        requestMessage
                        invalidRequestError
                    }
                    response {
                        Id
                        responseDateTime
                        statusCode
                        reasonPharse
                        setcookieHeader
                        headerJson
                        body
                        contentLength
                        responseDisplayText
                    }
                }
            }
        }
    `

        const [ok, err, resp] = await this._wc.graphql(query)

        if(!ok)
        {
            return [ok, err, []];
        }

        const gqlOK = resp?.data.data.fuzzRequestResponse.ok;
        //const err = resp?.data.data.fuzzRequestResponse.error;
        const result = resp?.data.data.fuzzRequestResponse.result;

        return [gqlOK, '', result];
    }

    private propMap(obj: any, mappedObject: any ) {

        if(obj == undefined)
        {
            return;
        }
        
        const thisObj = this;

        const keys = Object.keys( obj )
        
        for (const key of keys) {
            if (obj[ key ] == null)
                continue;
            if(Array.isArray(obj[ key ] ))
            continue;
            else if ( typeof obj[ key ] === 'object' ) {
                // If it's an object, let's go recursive
                thisObj.propMap(obj[ key ], mappedObject );
            }
            else {
                // If it's not, add a key/value
                mappedObject[ key ] = obj[ key ];
            }
        }
    }
}