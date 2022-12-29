import * as vscode from "vscode";
import * as fs from 'fs';
import * as path from 'path';
import {VSCEventLogger} from './Logger';
import { timingSafeEqual } from "crypto";

export class VuejsPanel {
	
	private vuejsDistFolder = 'dist/webview';
    public static currentPanel: VuejsPanel | undefined;
    private _vuejsPanel: vscode.WebviewPanel;
    private _extensionPath: string
    private _disposables: vscode.Disposable[] = [];
	private static _context: vscode.ExtensionContext;
	private static _eventlogger : VSCEventLogger;

    public static createOrShow(context: vscode.ExtensionContext, eventlogger: VSCEventLogger, extensionPath: string) {
		const column = vscode.window.activeTextEditor ? vscode.window.activeTextEditor.viewColumn : undefined;

		this._context = context;
		this._eventlogger = eventlogger;

		// If we already have a panel, show it.
		// Otherwise, create a new panel.
		if (VuejsPanel.currentPanel) {
			VuejsPanel.currentPanel._vuejsPanel.reveal(column);
		} else {
			VuejsPanel.currentPanel = new VuejsPanel(extensionPath, column || vscode.ViewColumn.One);
		}
	}


    public constructor(extensionPath: string, column: vscode.ViewColumn)
    {
		try {
			VuejsPanel._eventlogger.log('intializing webview')

			this._extensionPath = extensionPath;
	
			// Otherwise, create a new panel.
			this._vuejsPanel = vscode.window.createWebviewPanel(
				'vuejs',
				'Fuzzie',
				column || vscode.ViewColumn.One,
				{
					enableScripts: true,
					localResourceRoots: [
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder)),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'assets')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'fonts')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'img')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/app.js')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/app.js.map')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/chunk-vendors.js')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/chunk-vendors.js.map')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/webfontloader.js')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/webfontloader.js.map'))
					],
					portMapping: [
						{ webviewPort: 50001, extensionHostPort: 50001}
					]
				}
			);
	
			this._vuejsPanel.webview.onDidReceiveMessage(
				message => {
				  switch (message.command) {
					case 'read-file-content':
					  
						const type = message.type;
						const content = message.content;

	
						fs.readFile(content, 'utf8', function(err, data){
			
							this._vuejsPanel.webview.postMessage({ command: 'file-content-result', type: type, content: data});
						});
					
					  	return;
				  }
				},
				undefined,
				VuejsPanel._context.subscriptions
			  );
		
	
			let html = this._getHtmlForWebview()
			
			this._vuejsPanel.webview.html = html
	
			// Listen for when the panel is disposed
			// This happens when the user closes the panel or when the panel is closed programatically
			this._vuejsPanel.onDidDispose(() => this.dispose(), null, this._disposables);

		} catch (error) {
			VuejsPanel._eventlogger.log(`error when creating webview ${error}`);
		}
    }

    public readFile(path: string) {
		// Send a message to the webview webview.
		// You can send any JSON serializable data.
		
	}

	public dispose() {

		VuejsPanel.currentPanel = undefined

		// Clean up our resources
		this._vuejsPanel.dispose();

		while (this._disposables.length) {
			const x = this._disposables.pop();
			if (x) {
				x.dispose();
			}
		}
	}

    private _getHtmlForWebview() {

		const appjsPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/app.js'));
		const appjswebviewUrl = this._vuejsPanel.webview.asWebviewUri(appjsPathOnDisk);
		//const appjsUri = appjsPathOnDisk.with({ scheme: 'vscode-resource' });

        const chunkVendorsPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/chunk-vendors.js'));
		const chunkVendorsWebviewUrl = this._vuejsPanel.webview.asWebviewUri(chunkVendorsPathOnDisk);
		//const chunkVendorsUri = chunkVendorsPathOnDisk.with({ scheme: 'vscode-resource' });

		const vendorWebFontLoaderPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/webfontloader.js'));
		const vendorWebFontLoaderWebviewUrl = this._vuejsPanel.webview.asWebviewUri(vendorWebFontLoaderPathOnDisk);
		// const vendorWebFontLoaderUri = vendorWebFontLoaderPathOnDisk.with({ scheme: 'vscode-resource' });

		const appCSSPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css/app.css'));
		const appCSSWebviewUrl = this._vuejsPanel.webview.asWebviewUri(appCSSPathOnDisk);
		// const appCSSUri = appCSSPathOnDisk.with({ scheme: 'vscode-resource' });

		const vendorCSSPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css/chunk-vendors.css'));
		const vendorCSSWebviewUrl = this._vuejsPanel.webview.asWebviewUri(vendorCSSPathOnDisk);
		// const vendorCSSUri = vendorCSSPathOnDisk.with({ scheme: 'vscode-resource' });
		

		// Use a nonce to whitelist which scripts can be run
		const nonce = getNonce();

		//return `<!doctype html><html lang=""><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fuzzie</title><script defer="defer" src="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/js/chunk-vendors.js"></script><script defer="defer" src="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/js/app.js"></script><script defer="defer" src="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/css/webfontloader.js"></script><link href="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/css/app.css" rel="stylesheet"><link href="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/css/chunk-vendors.css" rel="stylesheet"></head><body><div id="app"></div></body></html>`;
		return `<!doctype html>
		<html lang="">
			<head>
				<meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge">
				<meta name="viewport" content="width=device-width,initial-scale=1">
				<title>Fuzzie</title>
				<script defer="defer" src="${chunkVendorsWebviewUrl}"></script>
				<script defer="defer" src="${appjswebviewUrl}"></script>
				<script defer="defer" src="${vendorWebFontLoaderWebviewUrl}"></script>
				<link href="${appCSSWebviewUrl}" rel="stylesheet">
				<link href="${vendorCSSWebviewUrl}" rel="stylesheet">
				<script src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
			</head>
			<body>
				<div id="app"></div>
			</body>
		</html>`;
	}
}

function getNonce() {
	let text = "";
	const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
	for (let i = 0; i < 32; i++) {
		text += possible.charAt(Math.floor(Math.random() * possible.length));
	}
	return text;
}
