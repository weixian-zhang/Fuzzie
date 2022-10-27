import * as vscode from 'vscode';

export default class StateManager
{
    private context: vscode.ExtensionContext;

    public constructor(context: vscode.ExtensionContext)
    {
        this.context = context;
    }

    public get (key: string) {
        const val  = this.context.globalState.get(key);
        return val
    }
    
    public async set(key:string, data: string) {
        await this.context.globalState.update(key, data)
    }
}