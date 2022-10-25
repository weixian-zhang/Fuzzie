import WebSocket from 'ws';
import ReconnectingWebSocket from 'reconnecting-websocket'
import axios from 'axios'
import EventLogger from './Logger';

export default class WebClient
{
    private _retryInternalMillisec = 3000;
    private _gqlAddress = "http://localhost:50001/graphql";
    private _wsAddress = "ws://localhost:50001/ws";
    private _ws: ReconnectingWebSocket;
    private _logger: EventLogger;

    public constructor()
    {
        this._logger = new EventLogger();
        this._ws = new ReconnectingWebSocket(this._wsAddress, "", {WebSocket: WebSocket});
        this.initWSClient();
    }

    private initWSClient()
    {

        this._ws.addEventListener("error", (err) => {
            this._logger.log(err.message)
        });

        this._ws.addEventListener('open', () => {
            this._logger.log('connected to fuzzer websocket server')
        });

        this._ws.addEventListener('close', () => {
            this._logger.log(`websocket client closed, retrying...`)
        });

        this._ws.addEventListener('message', (event) => {
            this._logger.log(event.data.toString());
        });
    }

    public async isFuzzerWebsocketServerRunning(): Promise<boolean>
    {
        return new Promise((resolve, reject) => {
            const timer = setInterval(() => {

                if(this._ws.readyState === 1) {
                    clearInterval(timer)
                    resolve(true);
                }
            }, this._retryInternalMillisec);
        })
    }

    public async isGraphQLServerAlive()
    {
        return new Promise((resolve, reject) => {
            const timer = setInterval(() => {

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
                            clearInterval(timer);
                            resolve(true);
                       }
                          
                   })
                   .catch(err => {
                       this._logger.log(err.message);
                   });

            }, this._retryInternalMillisec);
        })

        
    }
    
}