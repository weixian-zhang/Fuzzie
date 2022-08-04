// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

var openapi3Url = ""

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	
	console.log('Congratulations, your extension "wxz-fuzzie" is now active!');

	let disposable = vscode.commands.registerCommand('fuzzie.apischema.openapi3.url', callFuzzie);

	context.subscriptions.push(disposable);
}

async function callFuzzie(apiSchemaSource: string) {
	var inputOpenApi3Url: any = await vscode.window.showInputBox({
		placeHolder: "Enter OpenAPI 3 spec Url",
	  });

	if(inputOpenApi3Url !== undefined){

		vscode.window.showInformationMessage(inputOpenApi3Url);

	  }
}

// this method is called when your extension is deactivated
export function deactivate() {}
