import * as vscode from 'vscode';

export default class EventLogger
{
    private _outputWindow: vscode.OutputChannel;

    public constructor()
    {
        this._outputWindow = vscode.window.createOutputChannel("Fuzzie");
		    
    }

    public log(message: string)
    {
        this._outputWindow.appendLine(JSON.stringify(new EventLog(message)));
    }
}

class EventLog {
    public message: string = ""
    public datetime: Date = new Date()
    public constructor(message: string)
    {
        this.message = message;

    }
}