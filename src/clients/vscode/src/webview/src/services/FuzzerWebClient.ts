import { ApiFuzzContext } from "../Model";
import axios from "axios";
import { DocumentNode, print } from 'graphql';
import gql from 'graphql-tag';

export default class FuzzerWebClient
{
    private gqlUrl = 'http://localhost:50001/graphql';


    
    //const wsUrl: string = 'ws://localhost:50001/ws';

    
    public async getFuzzContexts(): Promise<any> {

        const query = `query {
            fuzzContexts {
                Id
                datetime
                apiDiscoveryMethod,  
                isanonymous,
                name,
                requestTextContent,
                requestTextFilePath,
                openapi3FilePath,
                openapi3Url,
                openapi3Content,
                basicUsername,
                basicPassword,
                bearerTokenHeader,
                bearerToken,
                apikeyHeader,
                apikey,
                hostname,
                port,
                fuzzcaseToExec,
                authnType
                fuzzCaseSetRuns {
                    fuzzCaseSetRunsId
                    fuzzcontextId
                    startTime
                    endTime
                    status
                }
            }
        }`
        
        try {

            const response = await axios.post(this.gqlUrl, {query});
            
            if(response.data.data != undefined)
            {
                return response.data.data.fuzzContexts;
            }
            else
            {
                return [];
            }
            

        } catch (err) {
            //TODO: Handle Error Here
            console.error(err);
            return [];
        }        
    }

    public async getFuzzCaseSetWithRunSummary(fuzzcontextId: string): Promise<any> {

        const query = `
                        query {
                            fuzzCaseSetWithRunSummary(fuzzcontextId: "${fuzzcontextId}") {
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
                            }
                        }
                        `
        
        try {

            const response = await axios.post(this.gqlUrl, {query});

            if(response.data.data != null)
            {
                return response.data.data.fuzzCaseSetWithRunSummary;
            }
            else
            {
                return [];
            }
            
            

        } catch (err) {
            //TODO: Handle Error Here
            console.error(err);
            return [];
        }        
    }

    public async createNewApiFuzzContext(fuzzcontext: ApiFuzzContext): Promise<any> {

        const query = `
            mutation newApiFuzzContext {
                newApiFuzzContext(
                            apiDiscoveryMethod: "${fuzzcontext.apiDiscoveryMethod}",
                            isanonymous: ${fuzzcontext.isanonymous},
                            name:"${fuzzcontext.name}",
                            requestTextContent:"${fuzzcontext.requestTextContent}",
                            requestTextFilePath:"${fuzzcontext.requestTextFilePath}",
                            openapi3FilePath:"${fuzzcontext.openapi3FilePath}",
                            openapi3Url:"${fuzzcontext.openapi3Url}",
                            openapi3Content:"${fuzzcontext.openapi3Content}",
                            basicUsername:"${fuzzcontext.basicUsername}",
                            basicPassword:"${fuzzcontext.basicPassword}",
                            bearerTokenHeader:"${fuzzcontext.bearerTokenHeader}",
                            bearerToken:"${fuzzcontext.bearerToken}",
                            apikeyHeader:"${fuzzcontext.apikeyHeader}",
                            apikey:"${fuzzcontext.apikey}",
                            hostname:"${fuzzcontext.hostname}",
                            port:${fuzzcontext.port},
                            fuzzcaseToExec: ${fuzzcontext.fuzzcaseToExec},
                            authnType: "${fuzzcontext.authnType}"){
                ok
                error
                }
            }
        `
                        
        
        try {

            const response = await axios.post(this.gqlUrl, {query});

            //http error
            if(response.data.errors != null && response.data.errors.length > 0)
            {
                //TODO: log graphql errors
                const errMsg = this.getErrorMsg(response.data.errors)
                console.log(errMsg);

                return {ok: false, error:errMsg, fuzzcontext: null};
            }

            // graphql result including error
            if(response.data != null)
            {
                const result = response.data.data.newApiFuzzContext

                return {
                        ok: result.ok,
                        error: result.error,
                        apiFuzzContext: result.apiFuzzContext
                    };
            }
            
            return {
                ok: true,
                error: '',
                apiFuzzContext: {}
            };
            

        } catch (err) {
            //TODO: Handle Error Here
            console.error(err);
            return {
                ok: false,
                error: err,
                apiFuzzContext: {}
            };
        }        
    }

    getErrorMsg(err: Array<any>) {

        let errMsg = '';

        if(err != null && err.length > 0)
        {
            err.forEach(e => {
                errMsg += e.message;
                errMsg += '\n';
            });
        }

        return errMsg
    }
}

