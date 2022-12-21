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
    }

    public send(message: unknown)
    {
        try {

            if(this._vscode == undefined) {
                return;
            }

            this._vscode.postMessage(message);

        } catch (error) {
            console.error(error);
        }
    }
}