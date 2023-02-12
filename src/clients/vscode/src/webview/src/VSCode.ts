export default class VSCode
{
    private vscode: any = undefined;

    constructor() {
        
        if ((window as any).vscode != undefined) {
            this.vscode = (window as any).vscode;
        }
    }

    public log(message: any)
    {
        try {

            if(this.vscode == undefined) {
                return;
            }
               
            this.vscode.postMessage({
                command: 'logging',
                message: `${message}`
            });
            
        
        } catch (error) {
            console.error(error);
        }
    }

    public saveFile(filename: string, content: string) {

        console.log(`this.vscode: ${this.vscode}`);

        if(this.vscode == undefined) {
            return;
        }

        this.vscode.postMessage({
            command: 'save-file',
            filename: filename,
            content: content
        })
    }

    public isVSCodeAPIUndefined() {
        if (this.vscode == undefined) {
            return true;
        }
        return false;
    }
}