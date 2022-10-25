import * as vscode from "vscode";
import * as fs from 'fs';
import * as path from 'path';

//https://github.com/microsoft/vscode-extension-samples/blob/main/webview-sample/src/extension.ts

export class WebAppPanel {

    private static _panel: vscode.WebviewPanel;
    private static _extensionPath: string

    private constructor() {
		
    }

    private static getWebviewOptions(extensionUri: vscode.Uri): vscode.WebviewOptions {
        return {
            // Enable javascript in the webview
            enableScripts: true,
    
            // And restrict the webview to only loading content from our extension's `media` directory.
            localResourceRoots: [
                vscode.Uri.file(path.join(extensionUri.path, 'vuejs-dist'))
            ]
        };
    }

    public static createOrShow(extensionUri: vscode.Uri)
    {
        WebAppPanel._extensionPath = extensionUri.path;

        const column = vscode.window.activeTextEditor
			? vscode.window.activeTextEditor.viewColumn
			: undefined;

        if (WebAppPanel._panel) {
			WebAppPanel._panel.reveal(column);
			return;
		}

		// Otherwise, create a new panel.
		// WebAppPanel._panel = vscode.window.createWebviewPanel(
		// 	'Fuzzie',
		// 	'Fuzzie',
		// 	column || vscode.ViewColumn.One,
		// 	this.getWebviewOptions(this._extensionUri),
		// );
        WebAppPanel._panel = vscode.window.createWebviewPanel(
            'catCoding',
            'Cat Coding',
            vscode.ViewColumn.One//,
            //WebAppPanel.getWebviewOptions(WebAppPanel._extensionUri)
          );


        
          let html = WebAppPanel._getHtmlForWebview()
          //fs.readFileSync(vscode.Uri.file(path.join(WebAppPanel._extensionUri.path, "vuejs-dist/index.html")).with({scheme: 'vscode-resource'}).fsPath, "utf-8");

          WebAppPanel._panel.webview.html = html
    }

    private static _getHtmlForWebview() {
		// const manifest = require(path.join(this._extensionPath, 'build', 'asset-manifest.json'));
		// const mainScript = manifest['files']['main.js'];
		// const mainStyle = manifest['files']['main.css'];

		const scriptPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, '../vuejs-dist', 'js/app.js'));
		const scriptUri = scriptPathOnDisk.with({ scheme: 'vscode-resource' });
		const stylePathOnDisk = vscode.Uri.file(path.join(this._extensionPath, '../vuejs-dist', 'css/app.css'));
		const styleUri = stylePathOnDisk.with({ scheme: 'vscode-resource' });

		// Use a nonce to whitelist which scripts can be run
		const nonce = getNonce();

		return `<!DOCTYPE html>
			<html lang="en">
			<head>
				<meta charset="utf-8">
				<meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no">
				<meta name="theme-color" content="#000000">
				<title>React App</title>
				<link rel="stylesheet" type="text/css" href="${styleUri}">
				<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src vscode-resource: https:; script-src 'nonce-${nonce}';style-src vscode-resource: 'unsafe-inline' http: https: data:;">
				<base href="${vscode.Uri.file(path.join(this._extensionPath, 'build')).with({ scheme: 'vscode-resource' })}/">
			</head>
			<body>
				<noscript>You need to enable JavaScript to run this app.</noscript>
				<div id="root"></div>
				
				<script nonce="${nonce}" src="${scriptUri}"></script>
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
