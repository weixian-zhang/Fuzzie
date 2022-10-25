// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from "child_process";
import {AppContext} from './AppContext';
import * as path from 'path';
import { VuejsPanel } from './VuejsPanel';
import FuzzerManager from './FuzzerManager';

var appcontext : AppContext;
var _outputWindow: vscode.OutputChannel;

var _pythonProcess: cp.ChildProcessWithoutNullStreams;
const _fuzzManager = new FuzzerManager();

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {
	
	log('Fuzzie is initializing');

	appcontext = new AppContext();

	initFuzzerPYZPath(context, appcontext);

	log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);

	
	context.subscriptions.push(   
		vscode.commands.registerCommand(
			'fuzzie.openwebview', () => 
				{
					VuejsPanel.createOrShow(context.extensionUri.path);
				}
		)
	);

	//TODO if fuzzer is NOT started, start Fuzzer
	startFuzzer(appcontext);

	await _fuzzManager.isFuzzerReady();
}

export async function deactivate(context: vscode.ExtensionContext) {
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
			log(`Fuzzer: ${data}`);
		});
		_pythonProcess.stdout?.on('data', (data: Uint8Array) => {
			log(`Fuzzer: ${data}`);
		});
		_pythonProcess.on('SIGINT',function(code){
			log(`Fuzzer: exiting ${code}`);
		});
		_pythonProcess.on('close', function(code){
			log(`Fuzzer: exiting ${code}`);
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

function log(message: string) {
	if(_outputWindow == null)
		_outputWindow = vscode.window.createOutputChannel("Fuzzie");

		_outputWindow.appendLine(message);
}

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





