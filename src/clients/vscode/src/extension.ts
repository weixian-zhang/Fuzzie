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

	context.subscriptions.push(   
		vscode.commands.registerCommand(
			'fuzzie.fuzzer.reset', () => 
				{
					killFuzzerProcess();
				}
		)
	);

	stateManager = new StateManager(context);
	
	eventlogger.log('Fuzzie is initializing');

	appcontext = new AppContext();

	initFuzzerPYZPath(context);

	eventlogger.log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);

	eventlogger.log('checking if fuzzer running');

	setInterval(monitorFuzzerReadiness, 2000);
}

export async function deactivate(context: vscode.ExtensionContext) {
	eventlogger.log('Fuzzie is deactivated, fuzzer is still running as background process');
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
			//const alive = response.data.data.fuzzerStatus.alive;
			fuzzerStartState = FuzzerStartState.Started
			return;
		}
		
	} catch (error: any) {
		if(fuzzerStartState == FuzzerStartState.NotStarted || fuzzerStartState == FuzzerStartState.Started) {
			fuzzerStartState = FuzzerStartState.Starting;
			startFuzzer();
		}
		
		eventlogger.log('fuzzer is either not started yet or was shut down, starting fuzzer now. \n This may take a while if you are using Fuzzie the first time.');
		return;
	}
}
        

async function startFuzzer() {

		try {
			
			let spawnOptions = { cwd: appcontext.fuzzerPYZFolderPath};

			if(_pythonProcess == undefined)
			{
				_pythonProcess = cp.spawn("python" , [appcontext.fuzzerPYZFilePath, "webserver", "start"], spawnOptions);

				const pid = _pythonProcess.pid

				stateManager.set('python-process-id', pid.toString());

				eventlogger.log(`Fuzzer process spawned with process id ${pid.toString()}`);
			}
				
				
			if(_pythonProcess != undefined) {
				_pythonProcess.stderr?.on('data', (data: Uint8Array) => {
					eventlogger.log(`Fuzzer: ${data}`, 'VSC');
				});
				_pythonProcess.stdout?.on('data', (data: Uint8Array) => {
					eventlogger.log(`Fuzzer: ${data}`, 'VSC');
				});
				_pythonProcess.on('SIGINT', onFuzzerExit);
				_pythonProcess.on('close', onFuzzerExit);
			}
		} catch (error) {
			
			//TODO: logging
			eventlogger.log(`error when starting fuzzer ${error}`);
			return;
		}
	
}

async function onFuzzerExit() {
	eventlogger.log('fuzzer exiting', 'VSC');
	stateManager.set('fuzzer.processid', undefined);
}

async function hardResetFuzzerIfExists() {
	killFuzzerProcess();
	startFuzzer();
}

async function killFuzzerProcess() {
	const pid = stateManager.get('fuzzer.processid');
	if(pid != undefined) {
		cp.spawn("taskkill", ["/pid", pid.toString(), '/f', '/t']);		 //on Windows
		process.kill(+pid);  											// on linux platform
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