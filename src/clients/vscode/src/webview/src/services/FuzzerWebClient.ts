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

            const gqlQuery = {
                "operationName": "",
                "query": query,
                "variables": {}
            };

            const axiosOpts = {
                "method": "POST",
                "body": JSON.stringify(query)
            };

            const response = await axios.post(this.gqlUrl, {query});
            
            return response.data.data.fuzzContexts;
            

        } catch (err) {
            // Handle Error Here
            console.error(err);
        }        
    }

}