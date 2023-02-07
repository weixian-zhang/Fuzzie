import * as vscode from 'vscode';
import {TelemetryClient} from 'applicationinsights';

export class VSCExtensionHostLogger
{
    private _outputWindow: vscode.OutputChannel;
    private telemetryClient;

    public constructor()
    {
        this.telemetryClient = LoggerHelper.createAppInsightsClient();

        this._outputWindow = vscode.window.createOutputChannel("Fuzzie - ExtensionHost");
		    
    }

    public log(message: string, source: string = "")
    {
        this._outputWindow.appendLine(`\n${JSON.stringify(new EventLog(message, source))}`);
    }

    public error(err: any) {
        if(typeof err === 'string') {
            this.telemetryClient.trackException({exception: new Error(err)});
        }
        else {
            this.telemetryClient.trackException({exception: err});
        }
    }
}

export class VSCWebViewLogger
{
    private _outputWindow: vscode.OutputChannel;

    public constructor()
    {
        this._outputWindow = vscode.window.createOutputChannel("Fuzzie - Webview/Fuzzer");
		    
    }

    public log(message: string, source: string = "")
    {
        this._outputWindow.appendLine(`\n${JSON.stringify(new EventLog(message, source))}`);
    }
}

export class LoggerHelper {
    public static createAppInsightsClient() {
        let appInsights = require("applicationinsights");
        appInsights.setup("InstrumentationKey=df5dcfcf-b50b-46af-a396-e9554aaa6539;IngestionEndpoint=https://eastasia-0.in.applicationinsights.azure.com/;LiveEndpoint=https://eastasia.livediagnostics.monitor.azure.com/")
            .setAutoDependencyCorrelation(true)
            .setAutoCollectRequests(true)
            .setAutoCollectPerformance(true, true)
            .setAutoCollectExceptions(true)
            .setAutoCollectDependencies(true)
            .setAutoCollectConsole(true, false)
            .setUseDiskRetryCaching(true)
            .setAutoCollectPreAggregatedMetrics(true)
            .setSendLiveMetrics(false)
            .setAutoCollectHeartbeat(false)
            .setAutoCollectIncomingRequestAzureFunctions(true)
            .setInternalLogging(false, true)
            .setDistributedTracingMode(appInsights.DistributedTracingModes.AI_AND_W3C)
            .enableWebInstrumentation(false)
            .start();

        return appInsights.defaultClient;
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