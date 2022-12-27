// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from "child_process";
import {AppContext} from './AppContext';
import * as path from 'path';
import { VuejsPanel } from './VuejsPanel';
import EventLogger from './Logger';
import StateManager from './StateManager';
import axios from "axios";
import { FuzzerStatus } from './Model';
import fetch from "node-fetch";

var gqlUrl = 'http://localhost:50001/graphql';

enum FuzzerStartState {
	NotStarted = 1,
	Starting = 2,
	Started = 3
}

var appcontext : AppContext;

var eventlogger = new EventLogger();

var stateManager:  StateManager;

var fuzzerStartState = FuzzerStartState.NotStarted;

var _pythonProcess: cp.ChildProcessWithoutNullStreams;


var gqlFuzzStatusQuery = `
            {
                fuzzerStatus {
                    timestamp,
                    alive,
                    isDataLoaded,
                    message,
                    webapiFuzzerInfo {
                        isFuzzing
                        fuzzContextId
                        fuzzCaseSetRunId
                    }
                } 
            }
        `;

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

	// stateManager = new StateManager(context);
	
	// eventlogger.log('Fuzzie is initializing');

	// appcontext = new AppContext();

	// initFuzzerPYZPath(context, appcontext);

	// eventlogger.log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);

	// eventlogger.log('checking if fuzzer running');

	try {


		// const a = fetch(gqlUrl, { 
		// 	method: 'POST',
		// 	Header: {
		// 	   'Content-Type': 'application/graphql'
		// 	},
		// 	body: gqlUrl
		//   })
		//   .then(response => response.json())
		//   .then(data => {
		// 	console.log('Here is the data: ', data);
		
		//   });

		//const todos = await axios.get('https://jsonplaceholder.typicode.com/todos');

		//const resp = await axios.post(gqlUrl, {gqlFuzzStatusQuery});
	
	} catch (error) {
		console.error(error.response.data);     // NOTE - use "error.response.data` (not "error")
	}



	//setInterval(monitorFuzzerReadiness, 1500);

	// if(!isFuzzerWSRunning)
	// {
	// 	eventlogger.log('fuzzer is not running, started fuzzer. This may take a few minutes the first time');
	// 	//startFuzzer(appcontext);
	// };
}

export async function deactivate(context: vscode.ExtensionContext) {
	eventlogger.log('Fuzzie is deactivated, fuzzer is still running as background process');
	//TODO and access:
		// get process pid from statemanager to and kill process
}

async function monitorFuzzerReadiness() {

	try {
		const response = await axios.post(gqlUrl, {gqlFuzzStatusQuery});

		if(this.responseHasData(response))
		{
			const result: FuzzerStatus = response.data.data.fuzzerStatus;
			if (result.alive) {
				fuzzerStartState = FuzzerStartState.Started;
				return;
			}
		}

		const [hasErr, err] = this.hasGraphqlErr(response);

		if(hasErr)
		{
			this.$logger.errorMsg(err);
			return ;
		}
		
	} catch (error: any) {
		if(fuzzerStartState == FuzzerStartState.NotStarted || fuzzerStartState == FuzzerStartState.Started) {
			fuzzerStartState = FuzzerStartState.Starting;
			startFuzzer(appcontext);
		}
		
		eventlogger.log('fuzzer is either not started yet or was shut down, starting fuzzer now. \n This may take a while if you are using Fuzzie the first time.');
		
		return;
	}
        
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
				eventlogger.log(`Fuzzer process spanwed with process id ${pid.toString()}`);
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





