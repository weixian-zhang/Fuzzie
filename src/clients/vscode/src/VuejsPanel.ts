import * as vscode from "vscode";
import * as fs from 'fs';
import * as path from 'path';
import {VSCExtensionHostLogger, VSCWebViewLogger} from './Logger';

export class VuejsPanel {
	
	private vuejsDistFolder = 'dist/webview';
    public static currentPanel: VuejsPanel | undefined;
    private _vuejsPanel: vscode.WebviewPanel;
    private _extensionPath: string
    private _disposables: vscode.Disposable[] = [];
	private static _context: vscode.ExtensionContext;
	private static _vscEHLogger : VSCExtensionHostLogger;
	private static _vscWBLogger : VSCWebViewLogger;

    public static createOrShow(context: vscode.ExtensionContext, 
		vscEHLogger: VSCExtensionHostLogger,
		vscWBLogger: VSCWebViewLogger, 
		extensionPath: string) {
		
		const column = vscode.window.activeTextEditor ? vscode.window.activeTextEditor.viewColumn : undefined;

		this._context = context;
		this._vscEHLogger = vscEHLogger;
		this._vscWBLogger = vscWBLogger;

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
			VuejsPanel._vscEHLogger.log('intializing webview')

			this._extensionPath = extensionPath;
	
			// Otherwise, create a new panel.
			this._vuejsPanel = vscode.window.createWebviewPanel(
				'vuejs',
				'Fuzzie',
				column || vscode.ViewColumn.One,
				{
					enableScripts: true,
					retainContextWhenHidden: true,
					localResourceRoots: [
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder)),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'assets')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'fonts')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'img')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css')),
						vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js')),
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

			let html = this._getHtmlForWebview()
			
			this._vuejsPanel.webview.html = html
	
			this._vuejsPanel.webview.onDidReceiveMessage(
				message => {
				  switch (message.command) {
					case 'save-file':

						const filename = message.filename;
						const content = message.content

						vscode.window
							.showSaveDialog({title: 'Save fuzz file', saveLabel:'Save fuzz file'})
							.then(fileInfos => {
								var path = fileInfos.path;
								if(path[0] == '/') {
									path = path.slice(1);
								}
							Buffer.from(content, 0);
							fs.writeFileSync(path, content, 'binary');
						});

						VuejsPanel._vscEHLogger.log(`saving fuzz file to ${filename}`);

					case 'logging':
						VuejsPanel._vscWBLogger.log(message.message);
				  }
				},
				undefined,
				VuejsPanel._context.subscriptions
			)	
		
			// Listen for when the panel is disposed
			// This happens when the user closes the panel or when the panel is closed programatically
			this._vuejsPanel.onDidDispose(() => this.dispose(), null, this._disposables);

		} catch (error) {
			VuejsPanel._vscEHLogger.error(error);
		}
    }

	// public saveFile(messageText: string) {
	// 	const dataUrl = messageText.split(',');
	// 	if (dataUrl.length > 0) {
	// 	  const u8arr = Base64.toUint8Array(dataUrl[1]);
	// 	  const workspaceDirectory = getWorkspaceFolder();
	// 	  const newFilePath = path.join(workspaceDirectory, 'VsCodeExtensionTest.png');

	// 	  fs.writeFile()
	// 	  writeFile(newFilePath, u8arr, () => {
	// 		vscode.window.showInformationMessage(`The file ${newFilePath} has been created in the root of the workspace.`);      
	// 	  });
	// 	}
	//   }
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
		
		//sourcemap
		const appjsPathSourceMapOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/app.js.map'));
		const appjsSourceMapWebviewUrl = this._vuejsPanel.webview.asWebviewUri(appjsPathSourceMapOnDisk);

        const chunkVendorsPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/chunk-vendors.js'));
		const chunkVendorsWebviewUrl = this._vuejsPanel.webview.asWebviewUri(chunkVendorsPathOnDisk);

		const chunkVendorsSourceMapOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/chunk-vendors.js.map'));
		const chunkVendorsSourceMapWebViewUrl = this._vuejsPanel.webview.asWebviewUri(chunkVendorsSourceMapOnDisk);

		const vendorWebFontLoaderPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/webfontloader.js'));
		const vendorWebFontLoaderWebviewUrl = this._vuejsPanel.webview.asWebviewUri(vendorWebFontLoaderPathOnDisk);
		
		//sourcemap
		const vendorWebFontLoaderSourceMapOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/webfontloader.js.map'));
		const vendorWebFontLoaderSourceMapWebviewUrl = this._vuejsPanel.webview.asWebviewUri(vendorWebFontLoaderSourceMapOnDisk);

		const appCSSPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css/app.css'));
		const appCSSWebviewUrl = this._vuejsPanel.webview.asWebviewUri(appCSSPathOnDisk);
		// const appCSSUri = appCSSPathOnDisk.with({ scheme: 'vscode-resource' });

		const vendorCSSPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css/chunk-vendors.css'));
		const vendorCSSWebviewUrl = this._vuejsPanel.webview.asWebviewUri(vendorCSSPathOnDisk);
		// const vendorCSSUri = vendorCSSPathOnDisk.with({ scheme: 'vscode-resource' });
		
		
		// Use a nonce to whitelist which scripts can be run
		const nonce = getNonce();

		//return `<!doctype html><html lang=""><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fuzzie</title><script defer="defer" src="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/js/chunk-vendors.js"></script><script defer="defer" src="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/js/app.js"></script><script defer="defer" src="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/css/webfontloader.js"></script><link href="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/css/app.css" rel="stylesheet"><link href="vscode-resource:/c%3A/Weixian/Projects/Fuzzie/src/clients/vscode/dist/webview/css/chunk-vendors.css" rel="stylesheet"></head><body><div id="app"></div></body></html>`;
		return `
			<html lang="en">
				<head>
					<meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge">
					<meta name="viewport" content="width=device-width,initial-scale=1">
					<title>Fuzzie</title>
				</head>
				<body>
					<div id="app"></div>
					
					<script nonce="${nonce}">
						window.vscode = acquireVsCodeApi();
					</script>

					// <script nonce="${nonce}" src="${chunkVendorsSourceMapWebViewUrl}"></script>
					// <script nonce="${nonce}" src="${vendorWebFontLoaderSourceMapWebviewUrl}"></script>
					// <script nonce="${nonce}" src="${appjsSourceMapWebviewUrl}"></script>
					
					

					<script nonce="${nonce}" src="${chunkVendorsWebviewUrl}"></script>
					<script nonce="${nonce}" src="${appjswebviewUrl}"></script>
					<script nonce="${nonce}" src="${vendorWebFontLoaderWebviewUrl}"></script>
					<link href="${appCSSWebviewUrl}" rel="stylesheet">
					<link href="${vendorCSSWebviewUrl}" rel="stylesheet">
					<script nonce="${nonce}" src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
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
