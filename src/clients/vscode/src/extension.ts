// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as cp from "child_process";
import {AppContext} from './AppContext';
import * as path from 'path';

var appcontext : AppContext;
var _outputWindow: vscode.OutputChannel;

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	
	log('Fuzzie is initializing');

	appcontext = new AppContext();
	appcontext.fuzzerPYZPath = initFuzzerPYZPath(context);

	log(`Fuzzer file path detected at ${appcontext.fuzzerPYZPath}`);

	let disposableOp3Url = vscode.commands.registerCommand('fuzzie.apirecognition.openapi3.url', gatherUserInputs);

	context.subscriptions.push(disposableOp3Url);

	log("starting up Fuzzie Fuzzer")

	startFuzzer();
}

async function gatherUserInputs(apiSchemaSource: string) {
	var inputOpenApi3Url: any = await vscode.window.showInputBox({
		placeHolder: "Enter OpenAPI 3 spec Url",
	  });

	if(inputOpenApi3Url !== undefined){

		vscode.window.showInformationMessage(inputOpenApi3Url);

	  }
}

async function startFuzzer() {

	const wsedit = new vscode.WorkspaceEdit();
    const workspaceFolders = vscode.workspace?.workspaceFolders;

	if(workspaceFolders != undefined && workspaceFolders.length > 0) {
		const path = workspaceFolders[0].uri.fsPath;
		log(path)
	}

	const cmd = `python ${appcontext.fuzzerPYZPath}`;

	let spawnOptions = { cwd: "c:\\Weixian\\Projects\\Fuzzie\\src\\clients\\vscode\\dist\\fuzzer"};
	var pythonProcess = cp.spawn("python" , ["c:\\Weixian\\Projects\\Fuzzie\\src\\clients\\vscode\\dist\\fuzzer\\fuzzie-fuzzer.pyz"], spawnOptions);

	if(pythonProcess != undefined) {
		pythonProcess.stderr?.on('data', (data: Uint8Array) => {
			log(`Fuzzer: ${data}`);
		});
		pythonProcess.stdout?.on('data', (data: Uint8Array) => {
			log(`Fuzzer: ${data}`);
		});
		pythonProcess.on('close', function(code){
			log(`Fuzzer: exiting ${code}`);
		});
	}
	


	// var msg = cp.exec(cmd, (err, stdout) => {
    //     console.log('result', err, stdout)
	// })

	// const pythonProcess = cp.spawnSync(cmd, {
	// 	shell: true,
	// 	encoding: 'utf8',
	//   });

	// var stdoutMsg = pythonProcess.stdout.toString();

	// while (stdoutMsg != "") {
	// 	log(`Fuzzer: ${stdoutMsg}`);
	// 	stdoutMsg = pythonProcess.stdout.toString();
	// }

	// const process = cp.spawnSync(cmd, {
	// 	shell: true,
	// 	encoding: 'utf8',
	//   });
	
	//   process.stdout.toString();

	// log("executing Fuzzer")
	// const pyFuzzer = spawn("python", []);

	// pyFuzzer.stderr.on("data", function(data) {
	// 	log(data.toString());
	// });

	// pyFuzzer.stdout.on("data", function(data) {
	// 	log(data.toString());
	// });

	// pyFuzzer.on('close', (code) => {
	// 	log(`Fuzzie Fuzzer exited with code ${code}`);
	//   });

}

const execShell = (cmd: string) =>
    new Promise<string>((resolve, reject) => {
        cp.exec(cmd, (err, out) => {
            if (err) {
                return reject(err);
            }
            return resolve(out);
        });
    });

function initFuzzerPYZPath(context: vscode.ExtensionContext) {
	var distFolder: string = "dist";
	var fuzzerPYZFileName : string = "fuzzer/fuzzie-fuzzer.pyz";
	var fuzzerPYZPath = path.join(context.extensionPath, distFolder, fuzzerPYZFileName);
	return fuzzerPYZPath;
}

function log(message: string) {
	if(_outputWindow == null)
		_outputWindow = vscode.window.createOutputChannel("Fuzzie");

		_outputWindow.appendLine(message);
}

// this method is called when your extension is deactivated
export function deactivate() {}
