import * as vscode from 'vscode';

export default class EventLogger
{
    private _outputWindow: vscode.OutputChannel;

    public constructor()
    {
        this._outputWindow = vscode.window.createOutputChannel("Fuzzie");
		    
    }

    public log(message: string, source: string = "")
    {
        this._outputWindow.appendLine(`\n${JSON.stringify(new EventLog(message, source))}`);
    }
}

class EventLog {
    public source: string = ""
    public message: string = ""
    public datetime: Date = new Date()
    public constructor(message: string, source: string = "")
    {
        this.message = message;
    }
}