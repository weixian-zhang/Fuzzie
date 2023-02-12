//https://github.com/winstonjs/winston/issues/287

import Utils from "./Utils";
import VSCode from "./VSCode";
import { ApplicationInsights } from '@microsoft/applicationinsights-web'

export default class Logger {

    private vscode;
    private _appinsights;

    public constructor() {
        this._appinsights = new ApplicationInsights({ config: {
            connectionString: 'InstrumentationKey=df5dcfcf-b50b-46af-a396-e9554aaa6539;IngestionEndpoint=https://eastasia-0.in.applicationinsights.azure.com/;LiveEndpoint=https://eastasia.livediagnostics.monitor.azure.com/'
          } });
        
          //disable dependency tracking
        this._appinsights.addDependencyInitializer((details) => {
            return false;
        });

        this._appinsights.loadAppInsights();

        this.vscode = new VSCode();
    }

    public info(message: string, source='') {

        console.log(message);

        this.vscode.log(message);
    }

    public errorMsg(message: string, source='') {
        console.log(message);

        this._appinsights.trackException(new Error(message), {source: 'webview'});

        //this._vscodeConsole.send(message);
    }

    public error(ex: any, source='') {
        
        if (ex instanceof Error) {
            if(!Utils.isNothing(ex) && !Utils.isNothing(ex.message) && !Utils.isNothing(ex.stack)) {

                const errMsg = `${ex.message}, ${ex.stack}`;

                console.log(errMsg);

                this._appinsights.trackException({ exception: ex }, {source: 'webview'});

                //this.vscode.log(errMsg);
            }
        }
        //ex is string
        else if (typeof ex === 'string') {
            console.log(ex);
            this._appinsights.trackException({ exception: new Error(ex) }, {source: 'webview'});
            //this._vscodeConsole.send(ex);
        }
        else {
            console.log(ex);
        }
        
    }
}