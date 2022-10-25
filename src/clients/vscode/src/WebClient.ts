import WebSocket from 'ws';

export default class WebClient
{
    private _gqlAddress = "http://localhost:50001";
    private _wsAddress = "wss://localhost:50001/ws";
    private _ws: WebSocket;

    public constructor()
    {
        this._ws = new WebSocket(this._wsAddress, "protocolOne");
    }

    public async connectToFuzzerWSServer(): Promise<boolean>
    {
        return new Promise((resolve, reject) => {
            const timer = setInterval(() => {
                if(this._ws.readyState === 1) {
                    clearInterval(timer)
                    resolve(true);
                }
            }, 10);
        })

    }
    
}