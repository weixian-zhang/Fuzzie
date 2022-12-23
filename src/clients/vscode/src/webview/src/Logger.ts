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
    }

    public errorMsg(message: string, source='') {
        console.log(message);
    }

    public error(ex: any, source='') {
        if(!Utils.isNothing(ex) && !Utils.isNothing(ex.message) && !Utils.isNothing(ex.stack)) {
            console.log(`${ex.message}, ${ex.stack}`);
        }
        
    }
}