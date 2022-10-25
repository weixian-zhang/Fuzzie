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
        
        const vuejsDistFolder = 'vuejs-dist'

		// Otherwise, create a new panel.
		WebAppPanel._panel = vscode.window.createWebviewPanel(
			'vuejs',
			'Fuzzie',
			column || vscode.ViewColumn.One,
			{
                enableScripts: true,
                localResourceRoots: [
				    vscode.Uri.file(path.join(this._extensionPath, vuejsDistFolder))
			    ]
            }
		);
        
        // this._panel = vscode.window.createWebviewPanel('vuejs', "React", {
        //     'Fuzzie',
		// 	'Fuzzie',
		// 	vscode.ViewColumn.One,

		// 	// Enable javascript in the webview
		// 	enableScripts: true,

		// 	// And restric the webview to only loading content from our extension's `media` directory.
		// 	localResourceRoots: [
		// 		vscode.Uri.file(path.join(this._extensionPath, 'build'))
		// 	]
		// });


        
          let html = WebAppPanel._getHtmlForWebview()
          //fs.readFileSync(vscode.Uri.file(path.join(WebAppPanel._extensionUri.path, "vuejs-dist/index.html")).with({scheme: 'vscode-resource'}).fsPath, "utf-8");

          WebAppPanel._panel.webview.html = html

          // Listen for when the panel is disposed
            // This happens when the user closes the panel or when the panel is closed programatically
            //this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }

    private static _getHtmlForWebview() {

        const vuejsDistFolder = 'vuejs-dist'

		const appjsPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, vuejsDistFolder, 'js/app.js'));
		const appjsUri = appjsPathOnDisk.with({ scheme: 'vscode-resource' });

        const chunkVendorsPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, vuejsDistFolder, 'js/chunk-vendors.js'));
		const chunkVendorsUri = chunkVendorsPathOnDisk.with({ scheme: 'vscode-resource' });

		const appCSSPathOnDisk = vscode.Uri.file(path.join(this._extensionPath,vuejsDistFolder, 'css/app.css'));
		const appCSSUri = appCSSPathOnDisk.with({ scheme: 'vscode-resource' });

		// Use a nonce to whitelist which scripts can be run
		const nonce = getNonce();

		return `<!doctype html><html lang=""><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1"><title>fuzzie</title><script defer="defer" src="${chunkVendorsUri}"></script><script defer="defer" src="${appjsUri}"></script><link href="${appCSSUri}" rel="stylesheet"></head><body><div id="app"></div></body></html>`;
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
