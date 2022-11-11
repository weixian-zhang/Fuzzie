// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from "child_process";
import {AppContext} from './AppContext';
import * as path from 'path';
import { VuejsPanel } from './VuejsPanel';
import EventLogger from './Logger';
import StateManager from './StateManager';
import WebSocket from 'ws';

var appcontext : AppContext;

var eventlogger = new EventLogger();
var stateManager:  StateManager;

var _pythonProcess: cp.ChildProcessWithoutNullStreams;


// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {

	context.subscriptions.push(   
		vscode.commands.registerCommand(
			'fuzzie.openwebview', () => 
				{
					VuejsPanel.createOrShow(context, eventlogger, context.extensionUri.path);
				}
		)
	);

	stateManager = new StateManager(context);
	
	eventlogger.log('Fuzzie is initializing');

	appcontext = new AppContext();

	initFuzzerPYZPath(context, appcontext);

	eventlogger.log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);

	
	

	eventlogger.log('checking if fuzzer running');

	const isFuzzerWSRunning = await isFuzzerRunning()

	if(!isFuzzerWSRunning)
	{
		eventlogger.log('fuzzer is not running, started fuzzer. This may take a few minutes the first time');
		//startFuzzer(appcontext);
	};
}

export async function deactivate(context: vscode.ExtensionContext) {
	eventlogger.log('Fuzzie is deactivated, fuzzer is still running as background process');
	//TODO and access:
		// get process pid from statemanager to and kill process
}

async function isFuzzerRunning(): Promise<boolean> {

	const wsAddress: string = "ws://localhost:50001/ws";

	var timesRun = 0;

        return new Promise((resolve) => {
            var interval = setInterval(() => {

                timesRun += 1;

                if(timesRun == 2)
                    clearInterval(interval);
                
                const ws = new WebSocket(wsAddress);

                ws.on("error", (err) => {
                });

                ws.on('open', () => {
                    eventlogger.log('Fuzzer is running')
                    resolve(true);
					ws.close();
                });

                ws.on('close', () => {
                    eventlogger.log(`fuzzer is not running`)
                    resolve(false);
                });
    
            }, 800);
        });
}

async function startFuzzer(appcontext: AppContext) {

	//TODO check if process is running
		//if running skip below

		try {

			let spawnOptions = { cwd: appcontext.fuzzerPYZFolderPath};

			if(_pythonProcess == undefined)
			{
				_pythonProcess = cp.spawn("python" , [appcontext.fuzzerPYZFilePath, "webserver", "start"], spawnOptions);

				const pid = _pythonProcess.pid
				if(pid != undefined)
					await stateManager.set('fuzzer/processid', pid.toString());
			}
				
				
			if(_pythonProcess != undefined) {
				_pythonProcess.stderr?.on('data', (data: Uint8Array) => {
					eventlogger.log(`Fuzzer: ${data}`);
				});
				_pythonProcess.stdout?.on('data', (data: Uint8Array) => {
					eventlogger.log(`Fuzzer: ${data}`);
				});
				_pythonProcess.on('SIGINT',function(code){
					eventlogger.log(`Fuzzer: exiting ${code}`);
				});
				_pythonProcess.on('close', function(code){
					eventlogger.log(`Fuzzer: exiting ${code}`);
				});
			}
		} catch (error) {
			
			//TODO: logging
			eventlogger.log(`error when starting fuzzer ${error}`);
			return;
		}
	
}

function initFuzzerPYZPath(vscodeContext: vscode.ExtensionContext, appcontext: AppContext) {
	var distFuzzerFolder: string = "dist/fuzzer";
	var fuzzerPYZFileName : string = "fuzzie-fuzzer.pyz";
	var cmdWorkingDir = path.join(vscodeContext.extensionPath, distFuzzerFolder )
	var fuzzerPYZFilePath = path.join(vscodeContext.extensionPath, distFuzzerFolder, fuzzerPYZFileName);

	appcontext.fuzzerPYZFilePath = fuzzerPYZFilePath;
	appcontext.fuzzerPYZFolderPath = cmdWorkingDir;
}





