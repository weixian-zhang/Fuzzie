## Fuzzie 

Fuzzie is a simple grey-box fuzz testing tool available as VSCode extension for fuzz testing REST API and GraphQL.  
The ability to fuzz test your REST and GraphQL APIs directly in an IDE brings about several advantages:

* fuzz tests guided by an intuitive WebView
* the ability to fuzz test very early during software development
* Being available in VSCode allows developers to conveniently fuzz test anytime without prior knowledge of fuzzing

### Prerequisites    

* Fuzzie requires Python 3.10 and above
* Fuzzie 

### Launching Fuzzie  

Open VSCode command palette (Ctrl + Shift + P) and search for "Fuzzie"  
![Alt text](https://github.com/weixian-zhang/Fuzzie/blob/main/doc/how%20to%20launch%20fuzzie.png)


### Using Fuzzie 

Fuzzie VSCode extension comes with a webview, everything from API and GraphQL discovery to fuzzing and analyzing test result can be done in webview.  

![Animation - Copy](https://user-images.githubusercontent.com/43234101/211010226-679c7e24-50a6-4a64-ad32-8fd3e40642fe.gif)

<br />  

#### Create a New API Fuzz Context

A Fuzz Context contains a list of cohesive "fuzz test cases" created by writing [HTTP Request Messages](#http-write-request-messages).  
Each test case contains HTTP verb, domain name, port, path, querystring, headers and body and Fuzzie make HTTP requests against all test cases in a Fuzz Context.  

#### How to write HTTP Request Messages  

Your REST and GraphQL endpoint schemas/contracts are described by writing Request Messages.  
The concept of Request Message is fully inspired by [Hau Chao's VSCode Rest Client project](https://github.com/Huachao/vscode-restclient#select-request-text)
Within a request message, you can replace any parameter in path, querystring, header, body with Fuzzie's built-in [Wordlists](#wordlist-types).  
By replacing wordlist {{ wordlist type }} with parameter, during fuzzing, Fuzzie will replace the wordlist with fuzz data depending on the type of wordlist.
example:  

#### Wordlist Types
The following are built-in wordlist-types, more will be added in future  
| WordList Type | Is Primitive wordlist type | Description   |
| ------------- |:-------------:| ------------- |
| {{ 'a quick brown fox' &#124; mutate }} | yes | your custom input that Fuzzie mutates |
| {{ string }} |  yes | naughty strings from [minimaxir/big-list-of-naughty-strings](https://github.com/minimaxir/big-list-of-naughty-strings) |
| {{ xss }} | yes | cross-site scripting strings from [danielmiessle/seclist](https://github.com/danielmiessler/SecLists) |
| {{ sqlinject }} | yes | sql-injection strings from danielmiessle/seclist |
| {{ bool }} | yes | boolean values and something naughty |
| {{ digit }} | yes | Integers, floats and something naughty |
| {{ char }} | yes | naughty chars |
| {{ image }} |  no | DALL-E images and a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist |
| {{ pdf }} |  no | Fuzzie generated fake PDF with a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist |
| {{ file }} |  no | naught payload from danielmiessle/seclist |
| <br>{{<br> '<br>custom file content<br>'<br> &#124; myfile('filename.csv')<br> }} | no | Custom file content within single quite '...' are uploaded as file<br>{{<br>'<br>this is a file content<br>{{string}} {{username}}<br>'<br> &#124; myfile("data.json")<br>}}  |
| {{ datetime }} | yes | date + time |
| {{ date }} | yes | date only |
| {{ time }} | yes | time only |
| {{ username }} | yes | hacked usernames from danielmiessler seclist |
| {{ password }} | yes | hacked password from danielmiessler seclist |
| {{ filename }} | yes | random file name and extensions |  

#### HTTP Request Message Syntax

<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/request-message-syntax-1.png" />





    
