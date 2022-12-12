
import FuzzerWebClient from "./FuzzerWebClient";
import { ApiFuzzContext, ApiFuzzcontextRuns, ApiFuzzContextUpdate, ApiFuzzCaseSetsWithRunSummaries } from "../Model";

export default class FuzzerManager
{
    private _wc: FuzzerWebClient;
    private isFuzzerWSConnected = false;
    private isFuzzerGraphQLRunning = true;
    
    public constructor()
    {
        this._wc = new FuzzerWebClient()
    }

    public async isFuzzerReady(): Promise<boolean>
    {
        //this.isFuzzerWSConnected = await this.webclient.connectToFuzzerWSServer();

        return true;
        //is websocket connected

        //
    }

    public async httpGetOpenApi3FromUrl(url: string): Promise<[boolean, string, string]> {

        const [ok, error, spec] = await this._wc.httpGetString(url)

        return [ok, error, spec];
    }

    public async getApiFuzzCaseSetsWithRunSummaries(fuzzcontextId: string): Promise<[boolean, string, [ApiFuzzCaseSetsWithRunSummaries|null]]> {
        
        const query = `
        query {
            fuzzCaseSetWithRunSummary(fuzzcontextId: "${fuzzcontextId}") {
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
                    file
                    http2xx
                    http3xx
                    http4xx
                    http5xx
                    completedDataCaseRuns
                }
            }
        }
        `;

        const [ok, err, resp] = await this._wc.graphql(query)

        if(!ok)
        {
            return [ok, err, [null]];
        }

        const gqlOK = resp?.data.data.fuzzCaseSetWithRunSummary.ok;
        const error = resp?.data.data.fuzzCaseSetWithRunSummary.error;
        const result = resp?.data.data.fuzzCaseSetWithRunSummary.result;

        return [gqlOK, error, result];
    }

    public async saveFuzzCaseSetSelected(fuzzCaseSetSelected): Promise<[boolean, string]> {

        let fcsStr = JSON.stringify(fuzzCaseSetSelected);

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

    public async updateApiFuzzContext(fuzzcontext: ApiFuzzContextUpdate): Promise<[boolean, string]>
    {
        const [ok, error] = await this._wc.updateApiFuzzContext(fuzzcontext);

        return [ok, error];
    }

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