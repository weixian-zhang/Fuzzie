import * as vscode from "vscode";
import * as fs from 'fs';
import * as path from 'path';


export class VuejsPanel {
	private vuejsDistFolder = 'dist/webview';
    public static currentPanel: VuejsPanel | undefined;
    private _panel: vscode.WebviewPanel;
    private _extensionPath: string
    private _disposables: vscode.Disposable[] = [];

    public static createOrShow(extensionPath: string) {
		const column = vscode.window.activeTextEditor ? vscode.window.activeTextEditor.viewColumn : undefined;

		// If we already have a panel, show it.
		// Otherwise, create a new panel.
		if (VuejsPanel.currentPanel) {
			VuejsPanel.currentPanel._panel.reveal(column);
		} else {
			VuejsPanel.currentPanel = new VuejsPanel(extensionPath, column || vscode.ViewColumn.One);
		}
	}


    public constructor(extensionPath: string, column: vscode.ViewColumn)
    {
        this._extensionPath = extensionPath;

		// Otherwise, create a new panel.
		this._panel = vscode.window.createWebviewPanel(
			'vuejs',
			'Fuzzie',
			column || vscode.ViewColumn.One,
			{
                enableScripts: true,
                localResourceRoots: [
				    vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder)),
					vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'assets')),
					vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'fonts')),
					vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'img'))
			    ]
            }
		);

        let html = this._getHtmlForWebview()
        
        this._panel.webview.html = html

        // Listen for when the panel is disposed
        // This happens when the user closes the panel or when the panel is closed programatically
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }

    public sendMessageToWebview() {
		// Send a message to the webview webview.
		// You can send any JSON serializable data.
		this._panel.webview.postMessage({ command: 'refactor' });
	}

	public dispose() {

		VuejsPanel.currentPanel = undefined

		// Clean up our resources
		this._panel.dispose();

		while (this._disposables.length) {
			const x = this._disposables.pop();
			if (x) {
				x.dispose();
			}
		}
	}

    private _getHtmlForWebview() {

		const appjsPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/app.js'));
		const appjsUri = appjsPathOnDisk.with({ scheme: 'vscode-resource' });

        const chunkVendorsPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'js/chunk-vendors.js'));
		const chunkVendorsUri = chunkVendorsPathOnDisk.with({ scheme: 'vscode-resource' });

		const vendorWebFontLoaderPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css/webfontloader.js'));
		const vendorWebFontLoaderUri = vendorWebFontLoaderPathOnDisk.with({ scheme: 'vscode-resource' });

		const appCSSPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css/app.css'));
		const appCSSUri = appCSSPathOnDisk.with({ scheme: 'vscode-resource' });

		const vendorCSSPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, this.vuejsDistFolder, 'css/chunk-vendors.css'));
		const vendorCSSUri = vendorCSSPathOnDisk.with({ scheme: 'vscode-resource' });

		

		// Use a nonce to whitelist which scripts can be run
		const nonce = getNonce();

		return `<!doctype html>
		<html lang="">
			<head>
				<meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge">
				<meta name="viewport" content="width=device-width,initial-scale=1">
				<title>Fuzzie</title>
				<script defer="defer" src="${chunkVendorsUri}"></script>
				<script defer="defer" src="${appjsUri}"></script>
				<script defer="defer" src="${vendorWebFontLoaderUri}"></script>
				<link href="${appCSSUri}" rel="stylesheet">
				<link href="${vendorCSSUri}" rel="stylesheet">
	
				
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
