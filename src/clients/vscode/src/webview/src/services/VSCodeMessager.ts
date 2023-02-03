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
            if(this._vscode != undefined) {
                this._vscode = acquireVsCodeApi();

                console.log(`VSCodeMessager, _vscode = acquireVsCodeApi`)
            }
        }
        else{
            console.log(`VSCodeMessager, acquireVsCodeApi is not a function`)
        }
    }

    public send(message: unknown)
    {
        try {
            
            if(this._vscode != undefined){
                this._vscode.postMessage(message);
            }
        
        } catch (error) {
            console.error(error);
        }
    }

    public sendFile(filename: string, content: string) {
        this._vscode?.postMessage({
            command: 'save-file',
            filename: filename,
            content: content
        })
    }
}