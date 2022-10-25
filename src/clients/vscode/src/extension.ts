// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from "child_process";
import {AppContext} from './AppContext';
import * as path from 'path';
import { WebAppPanel } from './WebAppPanel';

var appcontext : AppContext;
var _outputWindow: vscode.OutputChannel;

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	
	log('Fuzzie is initializing');

	appcontext = new AppContext();

	initFuzzerPYZPath(context, appcontext);

	log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);
	

	context.subscriptions.push(   
		vscode.commands.registerCommand(
			'fuzzie.open-webview', () => 
				{
					WebAppPanel.createOrShow(context.extensionUri);
				}
		)
	);
}

// this method is called when your extension is deactivated
export function openWebPanel() {
	deactivateFuzzie();
}


async function activateFuzzie()
{
	log("starting up Fuzzie Fuzzer. First time startup will take longer.")

	startFuzzer(appcontext);
}

async function deactivateFuzzie()
{
	log("deactivating Fuzzie: performing clean up");

	if(appcontext.pythonChildProcess != undefined) {
		appcontext.pythonChildProcess.kill();
	}
}

async function getOpenApiUrl() {
	var inputboxValue: any = await vscode.window.showInputBox({
		placeHolder: "OpenAPI 3 spec Url",
	  });

	if(inputboxValue !== undefined){
		vscode.window.showInformationMessage(inputboxValue);
	}
}

async function getOpenApiFilePath() {
	var inputboxValue: any = await vscode.window.showInputBox({
		placeHolder: "OpenAPI 3 spec file path",
	  });

	if(inputboxValue !== undefined){
		vscode.window.showInformationMessage(inputboxValue);
	}
}

async function getSingleRequestText() {
	return;
}

async function getRequestTextFilePath() {
	var inputboxValue: any = await vscode.window.showInputBox({
		placeHolder: "request text file path",
	  });

	if(inputboxValue !== undefined){
		vscode.window.showInformationMessage(inputboxValue);
	}
}


function startFuzzer(appcontext: AppContext) {

	let spawnOptions = { cwd: appcontext.fuzzerPYZFolderPath};
	var pythonProcess: cp.ChildProcessWithoutNullStreams = cp.spawn("python" , [appcontext.fuzzerPYZFilePath, "webserver", "start"], spawnOptions);
	
	if(pythonProcess != undefined) {
		pythonProcess.stderr?.on('data', (data: Uint8Array) => {
			log(`Fuzzer: ${data}`);
		});
		pythonProcess.stdout?.on('data', (data: Uint8Array) => {
			log(`Fuzzer: ${data}`);
		});
		pythonProcess.on('SIGINT',function(code){
			log(`Fuzzer: exiting ${code}`);
		});
		pythonProcess.on('close', function(code){
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


