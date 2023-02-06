// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from "child_process";
import {AppContext} from './AppContext';
import * as path from 'path';
import { VuejsPanel } from './VuejsPanel';
import {VSCExtensionHostLogger, VSCWebViewLogger} from './Logger';
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

var _vscEHLogger = new VSCExtensionHostLogger();
var _webviewLogger = new VSCWebViewLogger();

var stateManager:  StateManager;

var fuzzerStartState = FuzzerStartState.NotStarted;

var _pythonProcess: cp.ChildProcessWithoutNullStreams;

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {

	context.subscriptions.push(   
		vscode.commands.registerCommand(
			'fuzzie.openwebview', () => 
				{
					VuejsPanel.createOrShow(context,_vscEHLogger, _webviewLogger, context.extensionUri.path);
				}
		)
	);



	// context.subscriptions.push(   
	// 	vscode.commands.registerCommand(
	// 		'fuzzie.fuzzer.reset', () => 
	// 			{
	// 				hardResetFuzzerIfExists();
	// 			}
	// 	)
	// );
	

	stateManager = new StateManager(context);
	
	_vscEHLogger.log('Fuzzie is initializing');

	appcontext = new AppContext();

	initFuzzerPYZPath(context);

	_vscEHLogger.log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);

	_vscEHLogger.log('checking if fuzzer running');

	setInterval(monitorFuzzerReadiness, 2000);
}

export async function deactivate(context: vscode.ExtensionContext) {
	_vscEHLogger.log('Fuzzie webview is deactivated and fuzzer engine is shut down');
}

async function monitorFuzzerReadiness() {

	try {
		var query = `
            query {
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

		const response = await axios.post(gqlUrl, {query});

		if(gqlResponseHasData(response))
		{
			fuzzerStartState = FuzzerStartState.Started
			return;
		}
		
	} catch (error: any) {
		if(fuzzerStartState == FuzzerStartState.NotStarted || fuzzerStartState == FuzzerStartState.Started) {
			fuzzerStartState = FuzzerStartState.Starting;
			startFuzzer();

			_vscEHLogger.log('fuzzer is either not started yet or was shut down, starting fuzzer now. \n This may take a while if you are using Fuzzie the first time.');
		}
		
		return;
	}
}
        

async function startFuzzer() {

		try {
			
			let spawnOptions = { 
				cwd: appcontext.fuzzerPYZFolderPath,
				silent: true,
				detached: false,
			};

			if(_pythonProcess == undefined)
			{
				_vscEHLogger.log('spawning fuzzer child process', 'VSC');

				_pythonProcess = cp.spawn("python" , [appcontext.fuzzerPYZFilePath, "webserver", "start"], spawnOptions);

				const pid = _pythonProcess.pid;

				stateManager.set('python-process-id', pid.toString());

				_vscEHLogger.log(`fuzzer child process spawned with process id ${pid}`, 'VSC');

				_vscEHLogger.log(`Fuzzer process spawned with process id ${pid.toString()}`);
			}
				
			if(_pythonProcess != undefined) {

				process.on('SIGTERM', function () {
					_vscEHLogger.log('SIGTERM');
				  });

				_pythonProcess.stderr?.on('data', (data: Uint8Array) => {
					_vscEHLogger.log(`${data}`, 'Fuzzer');
				});
				_pythonProcess.stdout?.on('data', (data: Uint8Array) => {
					_vscEHLogger.log(`${data}`, 'Fuzzer');
				});
				_pythonProcess.on('SIGINT', onFuzzerExit);
				_pythonProcess.on('close', onFuzzerExit);
			}
		} catch (error) {
			
			//TODO: logging
			_vscEHLogger.log(`error when starting fuzzer ${error}`);
			return;
		}
	
}

async function onFuzzerExit() {
	_vscEHLogger.log('fuzzer process shutting down', 'VSC');
	stateManager.set('fuzzer.processid', undefined);
}

async function hardResetFuzzerIfExists() {
	killFuzzerProcess();
	startFuzzer();
}

async function killFuzzerProcess() {

	const pid = stateManager.get('fuzzer.processid');
	
	_vscEHLogger.log(`killing fuzzer process id ${pid}`, 'VSC')

	if(pid != undefined) {
		_vscEHLogger.log(`taskkill fuzzer process id ${pid}`, 'VSC')

		cp.spawn("taskkill", ["/pid", pid.toString(), '/f', '/t']);		 //on Windows

		_vscEHLogger.log(`process.kill fuzzer process id ${pid}`, 'VSC')

		process.kill(+pid);  		// on linux platform
												
		stateManager.set('fuzzer.processid', undefined);
	}
}

function initFuzzerPYZPath(vscodeContext: vscode.ExtensionContext) {
	var distFuzzerFolder: string = "dist/fuzzer";
	var fuzzerPYZFileName : string = "fuzzie-fuzzer.pyz";
	var cmdWorkingDir = path.join(vscodeContext.extensionPath, distFuzzerFolder )
	var fuzzerPYZFilePath = path.join(vscodeContext.extensionPath, distFuzzerFolder, fuzzerPYZFileName);

	appcontext.fuzzerPYZFilePath = fuzzerPYZFilePath;
	appcontext.fuzzerPYZFolderPath = cmdWorkingDir;
}

function gqlResponseHasData(resp) {
	if(resp != undefined && resp.data != undefined && resp.data.data != undefined)
	{
		return true;
	}
	return false;
}