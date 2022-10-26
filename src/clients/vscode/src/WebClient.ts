import WebSocket from 'ws';
import ReconnectingWebSocket from 'reconnecting-websocket'
import axios from 'axios'
import EventLogger from './Logger';

export default class WebClient
{
    private _retryInternalMillisec = 3000;
    private _gqlAddress: string = "http://localhost:50001/graphql";
    private _wsAddress: string = "ws://localhost:50001/ws";
    //private _ws: ReconnectingWebSocket;
    //private _ws: WebSocket;
    private _logger: EventLogger;

    public constructor()
    {
        this._logger = new EventLogger();
        //this._ws = new ReconnectingWebSocket(this._wsAddress, "", {WebSocket: WebSocket});
        //this.initWSClient();
    }

    // private initWSClient()
    // {
        
    //     this._ws.addEventListener("error", (err) => {
    //         this._logger.log(err.message)
    //     });

    //     this._ws.addEventListener('open', () => {
    //         this._logger.log('connected to fuzzer websocket server')
    //     });

    //     this._ws.addEventListener('close', () => {
    //         this._logger.log(`websocket client closed, retrying...`)
    //     });

    //     this._ws.addEventListener('message', (event) => {
    //         this._logger.log(event.data.toString());
    //     });
    // }

    async isFuzzerWebsocketServerRunning(): Promise<boolean>
    {
        var timesRun = 0;

        return new Promise((resolve) => {
            var interval = setInterval(() => {

                timesRun += 1;

                if(timesRun == 2)
                    clearInterval(interval);
                
                const ws = new WebSocket(this._wsAddress);

                ws.on("error", (err) => {
                    this._logger.log(err.message, 'ext-startup')
                });

                ws.on('open', () => {
                    this._logger.log('connected to fuzzer websocket server', 'ext-startup')
                    resolve(true);
                });

                ws.on('close', () => {
                    this._logger.log(`websocket client closed, retrying...`, 'ext-startup')
                    resolve(false);
                });
    
            }, 1000);
        });
        

        

        // return new Promise((resolve, reject) => {
        //     const timer = setInterval(() => {

        //         if(this._ws.readyState === 1) {
        //             clearInterval(timer)
        //             resolve(true);
        //         }
        //     }, this._retryInternalMillisec);
        // })
    }

    public async isGraphQLServerAlive()
    {
        var timesRun = 0;
        return new Promise((resolve) => {
            var interval = setInterval(() => {

                timesRun += 1;

                if(timesRun == 2)
                    clearInterval(interval);
                
                    axios({
                        url: this._gqlAddress,
                        method: 'post',
                        data: {
                          query: `
                            query {
                              alive
                            `
                        }
                      })
                        .then(response => {
                            if(response.status == 200)
                            {
                                resolve(true);
                            }
                                
                        })
                        .catch(err => {
                            this._logger.log(err.message, 'ext-startup');
                            resolve(false);
                        });
    
            }, 1000);
        });

        return new Promise((resolve, reject) => {
            const timer = setInterval(() => {

                

            }, 1000);
        })

        
    }
    
}