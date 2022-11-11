import type { WebviewApi } from "vscode-webview";

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

    public send(command: unknown, content: unknown)
    {
        try {

            if(this._vscode == undefined)
            {
                //TODO: log error
                console.log('VSCode API is undefine in webview');
                return;
            }

            this._vscode.postMessage({
                command: command,
                text: content
            });
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