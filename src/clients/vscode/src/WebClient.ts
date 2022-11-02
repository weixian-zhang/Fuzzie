import WebSocket from 'ws';
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

    async isFuzzerRunning(): Promise<boolean>
    {
        var timesRun = 0;

        return new Promise((resolve) => {
            var interval = setInterval(() => {

                timesRun += 1;

                if(timesRun == 2)
                    clearInterval(interval);
                
                const ws = new WebSocket(this._wsAddress);

                ws.on("error", (err) => {
                });

                ws.on('open', () => {
                    this._logger.log('Fuzzer is running')
                    ws.close();
                    resolve(true);
                });

                ws.on('close', () => {
                    this._logger.log(`fuzzer is not running`)
                    resolve(false);
                });
    
            }, 1000);
        });
        

    
    }
   
    
}