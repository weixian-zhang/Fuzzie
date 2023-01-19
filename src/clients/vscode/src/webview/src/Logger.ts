//https://github.com/winstonjs/winston/issues/287

import Utils from "./Utils";
import VSCodeMessager from "./services/VSCodeMessager";

export default class Logger {

    private _vscodeConsole;

    public constructor() {
        this._vscodeConsole = new VSCodeMessager();    
    }

    public info(message: string, source='') {
        console.log(message);
        this._vscodeConsole.send(message);
    }

    public errorMsg(message: string, source='') {
        console.log(message);
        this._vscodeConsole.send(message);
    }

    public error(ex: any, source='') {
        
        if (ex instanceof Error) {
            if(!Utils.isNothing(ex) && !Utils.isNothing(ex.message) && !Utils.isNothing(ex.stack)) {
                const errMsg = `${ex.message}, ${ex.stack}`;
                console.log(errMsg);
                this._vscodeConsole.send(errMsg);
            }
        }
        //ex is string
        else if (typeof ex === 'string') {
            console.log(ex);
            this._vscodeConsole.send(ex);
        }
        else {
            console.log(ex);
        }
        
    }
}