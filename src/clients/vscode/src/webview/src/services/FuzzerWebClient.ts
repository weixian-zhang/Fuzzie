import axios from "axios";

export default class FuzzerWebClient
{
    private gqlUrl = 'http://localhost:50001/graphql';


    
    //const wsUrl: string = 'ws://localhost:50001/ws';

    
    public async getFuzzContexts(): Promise<any> {

        const query = `query {
            fuzzContexts {
                Id
                datetime
                Id
                datetime
                name
                requestMessageText
                requestMessageFilePath
                openapi3FilePath
                openapi3Url
                hostname
                port
                fuzzMode
                fuzzcaseToExec
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

}