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
import * as fs from 'fs';
import * as stream from 'stream';
// import decompress from 'decompress';
var unzip = require('unzip-stream');

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

const fuzzerPackageName = "fuzzie-fuzzer.zip";


// this method is called when VSCode starts
// your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {

	//during vscode startup this function already activated
	
	context.subscriptions.push(   

		vscode.commands.registerCommand(
			'fuzzie.openwebview', () => 
				{
					VuejsPanel.createOrShow(context,_vscEHLogger, _webviewLogger, context.extensionUri.path);
				}
		)
	);

	stateManager = new StateManager(context);

	_vscEHLogger.log('Fuzzie is initializing');

	appcontext = new AppContext();

	initFuzzerPYZPath(context);

	startFuzzer();

	_vscEHLogger.log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);

	_vscEHLogger.log(`starting fuzzer`);
	

		// const commands = await vscode.commands.getCommands(true);

		// if (commands.indexOf('fuzzie.openwebview') == -1)
		// {
		// 	context.subscriptions.push(   

		// 		vscode.commands.registerCommand(
		// 			'fuzzie.openwebview', () => 
		// 				{
		// 					VuejsPanel.createOrShow(context,_vscEHLogger, _webviewLogger, context.extensionUri.path);
		// 				}
		// 		)
		// 	);

		// 	stateManager = new StateManager(context);
		
		// 	_vscEHLogger.log('Fuzzie is initializing');
		
		// 	appcontext = new AppContext();
		
		// 	initFuzzerPYZPath(context);
		
		// 	startFuzzer();
		
		// 	_vscEHLogger.log(`Fuzzer file path detected at ${appcontext.fuzzerPYZFilePath}`);
		
		// 	_vscEHLogger.log(`starting fuzzer`);
		// }
		
		
		
	
	
}

export async function deactivate(context: vscode.ExtensionContext) {
	killFuzzerProcess();
	stateManager.set('fuzzer.processid', undefined);
	_vscEHLogger.log('Fuzzie webview is deactivated and fuzzer engine is shut down');
}

async function unzipAndRunFuzzer() {
	// directory exists means fuzzer-fuzzie.zip has been uncompressed, then ignore unzhip process
	if (!fs.existsSync(appcontext.fuzzerExtractToPath)) {
		fs.mkdirSync(appcontext.fuzzerExtractToPath);
	}

	if(await isEmptyDir(appcontext.fuzzerExtractToPath)) {

		_vscEHLogger.log(`unzipping fuzzer at ${appcontext.fuzzerPYZFilePath}`);

		fs.createReadStream(appcontext.fuzzerPYZFilePath)
		.pipe(unzip.Extract({ path: appcontext.fuzzerDistFolder }))
		.on('error', (error)=>{
			_vscEHLogger.error(`error while unzipping fuzzer package: ${error}`);
		})
		.on('finish',()=>{
			_vscEHLogger.log(`fuzzer package unzipped at ${appcontext.fuzzerExtractToPath}`);
			startFuzzer();
		})
	}
	else {
		startFuzzer();
	}
}

async function isEmptyDir(path) {  
    try {
      const directory = await fs.opendirSync(path);
      const entry = await directory.read();
      await directory.close();

      return entry === null
    } catch (error) {
      return false
    }
}

function startFuzzer() {

	try {
		
		let spawnOptions = { 
			cwd: appcontext.fuzzerDistFolder,
			silent: true,
			detached: false,
		};

		_vscEHLogger.log('spawning fuzzer child process', 'VSC');

		_pythonProcess = cp.spawn("python" , [appcontext.fuzzerExtractToPath, "webserver", "start"], spawnOptions);
		
		const pid = _pythonProcess.pid;

		stateManager.set('fuzzer.processid', pid.toString());

		_vscEHLogger.log(`fuzzer child process spawned with process id ${pid}`, 'VSC');

		_vscEHLogger.log(`Fuzzer process spawned with process id ${pid.toString()}`);
			
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
			//_pythonProcess.on('SIGINT', onFuzzerExit);
			_pythonProcess.on('close', onFuzzerExit);
			_pythonProcess.on('exit', onFuzzerExit);
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

// async function hardResetFuzzerIfExists() {
// 	killFuzzerProcess();
// 	startFuzzer();
// }

function killFuzzerProcess() {

	if (_pythonProcess != undefined) {
		stateManager.set('fuzzer.processid', undefined);
		_pythonProcess.kill();
		_pythonProcess = undefined;
	}

	// const pid = stateManager.get('fuzzer.processid');
	
	// _vscEHLogger.log(`killing fuzzer process id ${pid}`, 'VSC')

	// if(pid != undefined) {
	// 	_vscEHLogger.log(`taskkill fuzzer process id ${pid}`, 'VSC')

	// 	cp.spawn("taskkill", ["/pid", pid.toString(), '/f', '/t']);		 //on Windows

	// 	_vscEHLogger.log(`process.kill fuzzer process id ${pid}`, 'VSC')

	// 	process.kill(+pid);  		// on linux platform
												
	// 	stateManager.set('fuzzer.processid', undefined);
	// }
}

function initFuzzerPYZPath(vscodeContext: vscode.ExtensionContext) {
	var distFuzzerFolder = "dist/fuzzer";
	//var fuzzerPYZFileName : string = "fuzzie-fuzzer";
	var distFuzzerFolderPath = path.join(vscodeContext.extensionPath, distFuzzerFolder);
	var fuzzerPYZFilePath = path.join(distFuzzerFolderPath, fuzzerPackageName);

	appcontext.fuzzerExtractToPath = path.join(distFuzzerFolderPath, "fuzzie-fuzzer");;
	//appcontext.fuzzerUnzippedFolder = path.join(distFuzzerFolderPath, "fuzzie-fuzzer");
	appcontext.fuzzerPYZFilePath = fuzzerPYZFilePath;
	appcontext.fuzzerDistFolder = distFuzzerFolderPath;
}

function gqlResponseHasData(resp) {
	if(resp != undefined && resp.data != undefined && resp.data.data != undefined)
	{
		return true;
	}
	return false;
}