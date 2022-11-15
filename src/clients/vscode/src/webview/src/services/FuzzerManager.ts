
import FuzzerWebClient from "./FuzzerWebClient";
import { ApiFuzzContext, ApiFuzzcontextRuns, ApiFuzzContextUpdate } from "../Model";
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