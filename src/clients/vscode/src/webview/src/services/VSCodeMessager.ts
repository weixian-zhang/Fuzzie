import type { WebviewApi } from "vscode-webview";


export class Message {
    public command = '';
    public type = '';
    public content = '';

    constructor(command, type, content) {
        this.command = command;
        this.type = type;
        this.content = content;
    }

    json()
    {
        return JSON.stringify(this);
    }
}


export default class VSCodeMessager
{
    private _vscode: WebviewApi<unknown> | undefined;

    private msgHandlers: any = {};

    constructor() {

        if (typeof acquireVsCodeApi === "function") {
            this._vscode = acquireVsCodeApi();
          }

        this.startListening();
    }

    public send(message: unknown)
    {
        try {

            if(this._vscode == undefined)
            {
                //TODO: log error
                console.log('VSCode API is undefine in webview');
                return;
            }

            this._vscode.postMessage(message);

        } catch (error) {
            //TODO: log error
            console.log(error);
        }
        
    }

    public subscribe(command: string, msgHandlerFunc: any) {

        this.msgHandlers[command] = msgHandlerFunc;
    }

    private startListening() {
        
        window.addEventListener('message', event => {
            
            try {
                const message = event.data; // The JSON data our extension sent
                const command = message.command;
                const content = message.content;

                const msgHandle = this.msgHandlers[command];

                msgHandle(content);
            } catch (error) {
                //TODO: log error
                console.log(error);
            }
        });
    }
}