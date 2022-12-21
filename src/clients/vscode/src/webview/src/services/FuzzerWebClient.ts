import { ApiFuzzContext, ApiFuzzContextUpdate } from "../Model";
import axios, {  AxiosError, AxiosResponse, } from "axios";
import {inject} from 'vue';

export default class FuzzerWebClient
{
    private gqlUrl = 'https://localhost:50001/graphql';
    private wsUrl = 'wss://localhost:50001';
    private _ws;
    private fuzzerEventSubscribers = {};  // dict with value as list  
    private axiosinstance;
    isWSConnected = false;
    $logger;

    public constructor() {
        this.$logger = inject('$logger'); 
    }

    connectWS() {
        this.connectWSInternal();
    }

    // private retryWSInternal() {



    //     setInterval(() => {
    //         if(!this.isWSConnected) {
    //             this.connectWSInternal();
    //         }
            
    //     }, 2000);
    // }

    private connectWSInternal = () => {
        
        try {

            this._ws = new WebSocket(this.wsUrl);

            this._ws.onopen = () => {

                this.isWSConnected = true;
    
                this.$logger.info('connected to fuzzer websocket server')
            };
          
            this._ws.onmessage = (e)  => {
              
                try {
                    const msg = e.data;

                    if (msg == '') {
                        this.$logger.errorMsg('received empty ws message from fuzzer')
                        return;
                    }

                    const jmsg = JSON.parse(msg)

                    const topic = jmsg.topic;
                    const data = jmsg.data;

                    const funcs = this.fuzzerEventSubscribers[topic];

                    funcs.forEach(f => {
                            f(data);
                    })
                } catch (err) {
                    console.error(err);
                    this.$logger.error(err);
                }
            };
          
            this._ws.onclose = (e) => {

                //TODO: log
                
                this.isWSConnected = false;
    
                this.$logger.info('cannot connect to fuzzer websocket server, retrying', e.reason);
                
                this._ws = null;
                setTimeout( () => {
                    this.connectWSInternal();
                }, 1500);
            };
          
            this._ws.onerror = (err) => {
              
              //TODO: log
              this.$logger.errorMsg('cannot connect to fuzzer websocket server, retrying');

              this._ws = null;

              if(this._ws != undefined){
                this._ws.close();
              }
            };
        } catch (error) {
            this.$logger.info(error);
        }
        
    }

    public subscribeWS(topic: string, func: any) {

        if(this.fuzzerEventSubscribers[topic] == undefined) {
            this.fuzzerEventSubscribers[topic] = []
        }
        
        const funcList = this.fuzzerEventSubscribers[topic];
        funcList.push(func);
    }
    
    public wsSend(data: string) {
        try {

            if(this._ws.connected) {
                this._ws.send(data);
            }
            
        } catch (error) {
            this.$logger.error(error);
        }
    }

    public async httpGetString(url: string): Promise<[boolean, string, string]> {

        try {

            const resp: AxiosResponse = await axios.get(url);
            const data = resp.data;

            if(data != undefined)
            {
                return [true, '', data];
            }

            return [false, '', ''];
            
        } catch (error) {
            this.$logger.error(error);
            return[false, this.errAsText(error as any[]), '']
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

            this.$logger.error(err);

            return [false, this.errAsText(err as any[]), []];
        }        
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
            const response = await axios.post(this.gqlUrl, {query});

            if(this.responseHasData(response))
            {
                const ok = response.data.data.fuzz.ok;
                const error = response.data.data.fuzz.msg;
                return [ok, error];
            }

            return [false, '']
            
        } catch (error: any) {
            return [false, error.message];
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
            this.$logger.error(err);
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
            this.$logger.error(err);
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
            this.$logger.error(err);
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

