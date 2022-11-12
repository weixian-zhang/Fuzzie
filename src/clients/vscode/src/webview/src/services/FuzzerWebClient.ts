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

    public async createNewApiFuzzContext(apiDiscoveryMethod: '',
                                            isanonymous: false,
                                            name: '',
                                            requestTextContent: '',
                                            requestTextFilePath: '',
                                            openapi3FilePath: '',
                                            openapi3Url: '',
                                            openapi3Content: '',
                                            basicUsername: '', 
                                            basicPassword: '', 
                                            bearerTokenHeader: '', 
                                            bearerToken: '', 
                                            apikeyHeader: '', 
                                            apikey: '', 
                                            hostname: '',
                                            port: 443,
                                            fuzzcaseToExec: 100,
                                            authnType: 'Anonymous'): Promise<any> {

        const query = `
        mutation discoverByFilePath {
            discoverByOpenapi3FilePath(
                          apiDiscoveryMethod: "${apiDiscoveryMethod}",
                          isanonymous: ${isanonymous},
                          name:"${name}",
                          requestTextContent:"${requestTextContent}",
                          requestTextFilePath:"${requestTextFilePath}",
                          openapi3FilePath:"${openapi3FilePath}",
                          openapi3Url:"${openapi3Url}",
                          openapi3Content:"${openapi3Content}",
                          basicUsername:"${basicUsername}",
                          basicPassword:"${basicPassword}",
                          bearerTokenHeader:"${bearerTokenHeader}",
                          bearerToken:"${bearerToken}",
                          apikeyHeader:"${apikeyHeader}",
                          apikey:"${apikey}",
                          hostname:"${hostname}",
                          port:${port},
                          fuzzcaseToExec: ${fuzzcaseToExec},
                          authnType: "${authnType}"){
              ok
              apiFuzzContext {
                  Id
                  datetime
                  name
              }
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

