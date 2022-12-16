import { ApiFuzzContext, ApiFuzzContextUpdate } from "../Model";
import axios, {  AxiosError, AxiosResponse, } from "axios";
import ReconnectingWebSocket from 'reconnecting-websocket';

export default class FuzzerWebClient
{
    private gqlUrl = 'https://localhost:50001/graphql';
    private wsUrl = 'wss://localhost:50001/ws';
    private _ws;
    private fuzzerEventSubscribers = {};  // dict with value as list  
    private axiosinstance;

    public constructor() {
        
        this._ws = new ReconnectingWebSocket(this.wsUrl, "", {WebSocket: WebSocket});
    }

    public connectWSServer()
    {
        this._ws.addEventListener("error", (err) => {
            //this._logger.log(err.message)
        });

        this._ws.addEventListener('open', () => {
            //this._logger.log('connected to fuzzer websocket server')
        });

        this._ws.addEventListener('close', () => {
            //this._logger.log(`websocket client closed, retrying...`)
        });

        this._ws.addEventListener('message', (event) => {

            const msg = event.data.toString()
            
            if (msg == "") {
                return;
            }
            
            // timestamp
            // data
            // topic
            const jmsg = JSON.parse(msg)

            if(jmsg.topic == '') {
                //TODO: log
                return
            }

            const funcList = this.fuzzerEventSubscribers[jmsg.topic];

            if (funcList == undefined){
                //TODO: logger log
                return;
            }
            
            funcList.forEach(func => {
                func(jmsg.data);
            });
        });
    }

    public subscribeWS(topic: string, func: any) {

        if(this.fuzzerEventSubscribers[topic] == undefined) {
            this.fuzzerEventSubscribers[topic] = []
        }
        
        const funcList = this.fuzzerEventSubscribers[topic];
        funcList.push(func);
    }
    
    //const wsUrl: string = 'ws://localhost:50001/ws'

    public async httpGetString(url: string): Promise<[boolean, string, string]> {

        try {

            const resp: AxiosResponse = await axios.get(url);
            const data = resp.data;

            if(data != undefined)
            {
                return [true, '', data];
            }

            return [false, '', ''];
            
        } catch (err) {
            //TODO: log error

            return[false, this.errAsText(err as any[]), '']
        }

    }

    
    public async getFuzzContexts(): Promise<any> {

        const query = `
            query {
                fuzzContexts {
                    ok,
                    error,
                    result {
                        Id
                        datetime
                        apiDiscoveryMethod,  
                        name,
                        requestTextContent,
                        requestTextFilePath,
                        openapi3FilePath,
                        openapi3Url,
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
                },
                
            }
        `
        
        try {

            const response = await axios.post(this.gqlUrl, {query});

            if(this.responseHasData(response))
            {
                const ok = response.data.data.fuzzContexts.ok;
                const error = response.data.data.fuzzContexts.error;
                const result = response.data.data.fuzzContexts.result;
                return [ok, error, result];
            }

            const [hasErr, err] = this.hasGraphqlErr(response);

            if(hasErr)
            {
                return [!hasErr, err, []];
            }

        } catch (err) {

            //TODO: Handle Error Here
            console.log(err);

            return [false, this.errAsText(err as any[]), []];
        }        
    }

    public async graphql(query): Promise<[boolean, string, AxiosResponse|null]> {
        
        try {

            const response = await axios.post(this.gqlUrl, {query});

            if(this.responseHasData(response))
            {
                return [true, '', response];
            }
            
            const [hasErr, err] = this.hasGraphqlErr(response);

            // graphql server reports error
            if(hasErr)
            {
                //TODO: log graphql errors

                return [false, err, null];
            }
            
            return [false, '', null];

        } catch (err) {
            //TODO: Handle Error Here
            console.error(err);
            return [false, this.errAsText(err as any), null];
        }  
    }

    public async updateApiFuzzContext(fuzzcontext: ApiFuzzContextUpdate): Promise<any> {
        const query = `
            mutation update_existing_api_fuzzcontext {
                updateApiFuzzContext(
                    fuzzContext: {
                            fuzzcontextId: "${fuzzcontext.fuzzcontextId}",
                            name:"${fuzzcontext.name}",
                            basicUsername:"${fuzzcontext.basicUsername}",
                            basicPassword:"${fuzzcontext.basicPassword}",
                            bearerTokenHeader:"${fuzzcontext.bearerTokenHeader}",
                            bearerToken:"${fuzzcontext.bearerToken}",
                            apikeyHeader:"${fuzzcontext.apikeyHeader}",
                            apikey:"${fuzzcontext.apikey}",
                            hostname:"${fuzzcontext.hostname}",
                            port:${fuzzcontext.port},
                            fuzzcaseToExec: ${fuzzcontext.fuzzcaseToExec},
                            authnType: "${fuzzcontext.authnType}"
                        }
                    )
                {
                    ok
                    error
                }
            }
        `
                        
        
        try {

            const response = await axios.post(this.gqlUrl, {query});

            if(this.responseHasData(response))
            {
                //TODO: log graphql errors

                const ok = response.data.data.updateApiFuzzContext.ok;
                const error = response.data.data.updateApiFuzzContext.error;

                return [ok, error];
            }
            
            const [hasErr, err] = this.hasGraphqlErr(response);

            if(hasErr)
            {
                return [!hasErr, err, []];
            }
            

        } catch (err) {
            //TODO: Handle Error Here
            console.error(err);
            return [false, this.errAsText(err as any)];
        }  
    }

    public async createNewApiFuzzContext(fuzzcontext: ApiFuzzContext): Promise<any> {

        const query = `
            mutation newApiFuzzContext {
                newApiFuzzContext(
                            apiDiscoveryMethod: "${fuzzcontext.apiDiscoveryMethod}",
                           
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

            const [hasErr, err] = this.hasGraphqlErr(response);

            if(hasErr)
            {
             
                //TODO: log graphql errors
                const errMsg = this.errAsText(response.data.errors)

                console.log(err);

                return {ok: false, error:err, fuzzcontext: null};
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

    resolveResult(resp): [boolean, string] {
        if(resp.data != null)
        {
            return [resp.data.ok, resp.data.error];
        }
        return [false, ''];
    }

    errAsText(err: Array<any>) {

        let errMsg = '';

        if(err instanceof AxiosError){
            errMsg = err.message;
        }

        if(err != null && err.length > 0)
        {
            err.forEach(e => {
                errMsg += e.message;
                errMsg += '\n';
            });
        }

        return errMsg
    }

    private responseHasData(resp) {
        if(resp != undefined && resp.data != undefined && resp.data.data != undefined)
        {
            return true;
        }
        return false;
    }

    private hasGraphqlErr(resp): [boolean, string] {
        if(resp.data.errors != null && resp.data.errors.length > 0)
        {
            const errMsg = this.errAsText(resp.data.errors);

            return [true, errMsg];
        }

        return [false, ''];
    }
}

