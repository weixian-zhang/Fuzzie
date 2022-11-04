
import FuzzerWebClient from "./FuzzerWebClient";
import { FuzzContext, ApiFuzzcontextRuns } from "../Model";
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

    public async getFuzzcontexts(): Promise<Array<FuzzContext>>
    {
        const data = await this._wc.getFuzzContexts()

        if(data == undefined)
            return []

        const fcs: Array<FuzzContext> = [];

        data.forEach(fc => {
            
            const newFC = new FuzzContext();

            this.propMap(fc, newFC);

            fcs.push(newFC);

            // newFC.Id = fc.Id;
            // newFC.datetime = fc.datetime;
            // newFC.name = fc.name;
            // newFC.requestMessageText = fc.requestMessageText;
            // newFC.requestMessageFilePath = fc.requestMessageFilePath;
            // newFC.openapi3FilePath = fc.;
            // newFC.openapi3Url = fc.;
            // newFC.hostname = fc.;
            // newFC.port = fc.;
            // newFC.fuzzMode = fc.;
            // newFC.fuzzcaseToExec = fc.;
            // newFC.authnType = fc.;

            if(fc.fuzzCaseSetRuns != undefined)
            {
                fc.fuzzCaseSetRuns.forEach(ele => {

                    const fcRun = new ApiFuzzcontextRuns();

                    this.propMap(ele, fcRun);

                    newFC.fuzzCaseSetRuns.push(fcRun);

                });
                
            }
            
            
        });

        return fcs;
    }

    private propMap(obj: any, mappedObject: any ) {
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

        // Object.keys( obj ).forEach( function( key ) {
        //     if (obj[ key ] == null)
        //         true;
        //     if(Array.isArray(obj[ key ] ))
        //         true;
        //     else if ( typeof obj[ key ] === 'object' ) {
        //         // If it's an object, let's go recursive
        //         thisObj.propMap(obj[ key ], mappedObject );
        //     }
        //     else {
        //         // If it's not, add a key/value
        //         mappedObject[ key ] = obj[ key ];
        //     }
        // } );
    }
}