// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from "child_process";
import {AppContext} from './AppContext';
import * as path from 'path';
import { VuejsPanel } from './VuejsPanel';
import WebClient from './WebClient';
import EventLogger from './Logger';

var appcontext : AppContext;

var eventlogger = new EventLogger();

var _pythonProcess: cp.ChildProcessWithoutNullStreams;

var _webclient = new WebClient()

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {
	
	eventlogger.log('Fuzzie is initializing');

	appcontext = new AppContext();

	initFuzzerPYZPath(context, appcontext);

	eventlogger.log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);

	
	context.subscriptions.push(   
		vscode.commands.registerCommand(
			'fuzzie.openwebview', () => 
				{
					VuejsPanel.createOrShow(context.extensionUri.path);
				}
		)
	);

	eventlogger.log('checking if fuzzer running');

	const isFuzzerRunning = true; // await _webclient.isFuzzerWebsocketServerRunning()

	const isFuzzerGraphQLRunning = await _webclient.isGraphQLServerAlive();

	if(!isFuzzerRunning || !isFuzzerGraphQLRunning)
	{
		eventlogger.log('fuzzer is not running, started fuzzer. This may tkae a few minutes before you can start to fuzz');
		startFuzzer(appcontext);
	};
}

export async function deactivate(context: vscode.ExtensionContext) {
	eventlogger.log('Fuzzie is deactivated');
	//TODO check if process is running
		//if running, kill process
}

function startFuzzer(appcontext: AppContext) {

	//TODO check if process is running
		//if running skip below

	let spawnOptions = { cwd: appcontext.fuzzerPYZFolderPath};

	if(_pythonProcess == undefined)
		_pythonProcess = cp.spawn("python" , [appcontext.fuzzerPYZFilePath, "webserver", "start"], spawnOptions);
		
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
	
}

function initFuzzerPYZPath(vscodeContext: vscode.ExtensionContext, appcontext: AppContext) {
	var distFuzzerFolder: string = "dist/fuzzer";
	var fuzzerPYZFileName : string = "fuzzie-fuzzer.pyz";
	var cmdWorkingDir = path.join(vscodeContext.extensionPath, distFuzzerFolder )
	var fuzzerPYZFilePath = path.join(vscodeContext.extensionPath, distFuzzerFolder, fuzzerPYZFileName);

	appcontext.fuzzerPYZFilePath = fuzzerPYZFilePath;
	appcontext.fuzzerPYZFolderPath = cmdWorkingDir;
}

// function log(message: string) {
// 	if(_outputWindow == null)
// 		_outputWindow = vscode.window.createOutputChannel("Fuzzie");

// 		_outputWindow.appendLine(message);
// }

// // this method is called when your extension is deactivated
// export function openWebPanel() {
// 	deactivateFuzzie();
// }


// async function activateFuzzie()
// {
// 	log("starting up Fuzzie Fuzzer. First time startup will take longer.")

	
// }

// async function deactivateFuzzie()
// {
// 	log("deactivating Fuzzie: performing clean up");

// 	if(appcontext.pythonChildProcess != undefined) {
// 		appcontext.pythonChildProcess.kill();
// 	}
// }

// async function getOpenApiUrl() {
// 	var inputboxValue: any = await vscode.window.showInputBox({
// 		placeHolder: "OpenAPI 3 spec Url",
// 	  });

// 	if(inputboxValue !== undefined){
// 		vscode.window.showInformationMessage(inputboxValue);
// 	}
// }

// async function getOpenApiFilePath() {
// 	var inputboxValue: any = await vscode.window.showInputBox({
// 		placeHolder: "OpenAPI 3 spec file path",
// 	  });

// 	if(inputboxValue !== undefined){
// 		vscode.window.showInformationMessage(inputboxValue);
// 	}
// }

// async function getSingleRequestText() {
// 	return;
// }

// async function getRequestTextFilePath() {
// 	var inputboxValue: any = await vscode.window.showInputBox({
// 		placeHolder: "request text file path",
// 	  });

// 	if(inputboxValue !== undefined){
// 		vscode.window.showInformationMessage(inputboxValue);
// 	}
// }





