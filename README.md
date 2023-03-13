## Fuzzie
[<img src="https://badgen.net/badge/vs-marketplace/0.12.0-preview/green" />](https://marketplace.visualstudio.com/items?itemName=wxz.wxz-fuzzie)

Fuzzie is a simple grey-box fuzz testing tool available as VSCode extension for fuzz testing REST API and GraphQL.  
The ability to fuzz test right in VSCode brings about several benefits:

* As early as while debugging APIs in VSCode running on localhost, you can concurrently use Fuzzie to fuzz test your APIs.  
  As Fuzzie also sends random unpredictable data, you can catch common bugs like unhandled input parameters early in development.
* fuzz tests guided by an intuitive WebView
* Being available in VSCode allows developers to conveniently fuzz test anytime without prior knowledge of fuzzing

### *Things to Note    

* Depending on [wordlist type](#2-write-http-request-messages), Fuzzie can send malicious strings from [SecList](https://github.com/danielmiessler/SecLists), recommend to use Fuzzie in test environments only
* requires Python 3.10 and above
* Fuzzie uses port 50001  
  fuzzer engine listens on http://localhost:50001 serving requests from webview
* Fuzzie uses sqlite internally to store all data, when upgrading to a newer extension version, previous data will not be retained
* On the very first launch, Fuzzie can take up to 10 - 12 secs to start up due to data loading 

### Launching Fuzzie  

Open VSCode command palette (Ctrl + Shift + P) and search for "Fuzzie"  
<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/how%20to%20launch%20fuzzie.png" />


### Using Fuzzie 

Fuzzie VSCode extension provides a webview for you to perform everything from API and GraphQL discovery to fuzzing and analyzing test result, all in a single place.  

<br /> 

![Animation - Copy](https://github.com/weixian-zhang/Fuzzie/blob/main/doc/fuzzie-webview-walkthrough.gif)

<br />  

#### 1. Webview Navigation  

<img src ="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/tutorial-fuzzie-webview.png" />

#### 2. Start by creating a  new API Fuzz Context

A Fuzz Context contains a list of cohesive "test cases" created by writing [HTTP Request Messages](#http-write-request-messages).  
Each test case contains HTTP verb, domain name, port, path, querystring, headers and body and Fuzzie make HTTP requests against all test cases in a Fuzz Context. 

<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/create-new-api-context.png" />  

#### 2. Write HTTP Request Messages  

Your REST and GraphQL target endpoints are described by writing Request Messages.  
The concept of Request Message is fully inspired by [Hau Chao's VSCode Rest Client project](https://github.com/Huachao/vscode-restclient#select-request-text).  

In request message, you can replace any parameter in path, querystring, header, body with Fuzzie's built-in [Wordlists](#wordlist-types).  
By replacing parameter with wordlist {{ wordlist type }}, during fuzzing, Fuzzie will replace the wordlist with fuzz data depending on the type of wordlist.

#### Wordlist Types
The following are built-in wordlist-types, more will be added in future  
Type = wordlist provides data  
Type = function acts on your provided custom data
| WordList Type | Is Primitive wordlist type | file upload | Description | Type |
| ------------- |-------------| -------------| ------------- | ------------- |
| {{ string }} |  yes | no | naughty strings from [minimaxir/big-list-of-naughty-strings](https://github.com/minimaxir/big-list-of-naughty-strings) | wordlist |
| {{ xss }} | yes | no | cross-site scripting strings from [danielmiessle/seclist](https://github.com/danielmiessler/SecLists) | wordlist |
| {{ sqlinject }} | yes | no | sql-injection strings from danielmiessle/seclist | wordlist |
| {{ bool }} | yes | no | boolean values and something naughty | wordlist |
| {{ digit }} | yes | no | Integers, floats and something naughty | wordlist |
| {{ char }} | yes | no | naughty chars | wordlist |
| {{ image }} |  no | yes | DALL-E images and a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist | wordlist |
| {{ pdf }} |  no | yes | Fuzzie generated fake PDF with a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist | wordlist |
| {{ file }} |  no | yes | naught payload from danielmiessle/seclist |
| <br>{{<br> '<br>custom file content<br>'<br> &#124; myfile('filename.csv')<br> }} | no | yes | Custom file content within single quite '...' are uploaded as file<br>{{<br>'<br>this is a file content<br>{{string}} {{username}}<br>'<br> &#124; myfile("data.json")<br>}}  | wordlist |
| {{ datetime }} | yes | no | date + time | wordlist |
| {{ date }} | yes | no | date only | wordlist |
| {{ time }} | yes | no | time only | wordlist |
| {{ username }} | yes | no | hacked usernames from danielmiessler seclist | wordlist |
| {{ password }} | yes | no | hacked password from danielmiessler seclist | wordlist |
| {{ filename }} | yes | no | random file name and extensions |  wordlist |
| {{ httppath }} | yes | no | discover directories and files |  wordlist |
| {{ numrange(start, end) }} | yes | no | increment number by 1 from start to end. <br>Example numrange(1, 5000): result is 1, 2, 3,...4999, 5000 | function |
| {{ 'a quick brown fox' &#124; <b>mutate</b> }} | yes | no | input will be mutated | function |
| {{ ['a', 'list', 'of', 'items' ]  &#124; <b>random</b> }} | yes | no | returns a random item from your list | function |
| {{ <br>'single string to be base64 encoded' &#124; <b>base64e</b> }}<br> <br>{{ ['list', 'of', 'items', 'to be base64 encoded'] &#124; <b>base64e</b> }}<br>  | yes | no | base64 encodes your input, or if a list is supplied, randomly pick an item and encodes it | function |
| {{ <br>'base64 encoded string to be decoded' &#124; <b>base64d</b> }}<br> <br>{{ ['list', 'of', 'encoded', 'items', 'to be base64 decoded'] &#124; <b>base64d</b> }}<br>  | yes | no | base64 encodes your input, or if a list is supplied, randomly pick an item and encodes it | function |

#### 2.1 Request Message Syntax  

Request message syntax follows [VSCode Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) closely.  
"Samples" drop-down button allows you to load different samples of request message where you can modify to suit your scenario  

* GraphQL request message has to include a special header: X-REQUEST-TYPE: GraphQL
* comments: // or #
* \#\#\# use for dividing request messages
* for myfile and mutate wordlists, your text must be within single quotes ' your string here'
  * single quotes within your custom string needs to be escaped with \.  
  For example below: **Don\\'t**
  ```
  <note>
    <to>{{ username }}</to>
    <from>{{ username }}</from>
    <heading>{{ 'Reminder' | mutate }}</heading>
    <body>{{ 'Don't forget me this weekend!' | mutate }}</body>
  </note>
  ```

<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/request-message-syntax-1.png" />  

##### GET

```
GET https://httpbin.org/get
?name={{username}}
&address={{string}}
&order=5
&mode={{string}}

```

##### GET with headers  
```
GET https://httpbin.org/get
?name={{username}}
&address={{string}}
&order=5
&mode={{string}}
Content-Type: application/xml
Authorization: {{ string }}
CustomHeader-1: {{ digit }}
CustomHeader-2: {{ filename }}
CustomHeader-3: {{ username }}
```

##### Upload files  

POST image

```
POST https://httpbin.org/post HTTP/1.1

{{ image('option-file-name.png') }}
```

POST PDF

```
POST https://httpbin.org/post HTTP/1.1

{{ pdf('option-file-name.pdf') }}
```  

POST [naughty payloads](https://github.com/danielmiessler/SecLists/tree/master/Payloads)

```
POST https://httpbin.org/post HTTP/1.1

{{ file('option-file-name.log') }}
```

POST <b>your custom file content</b> for example a CSV file

```
POST https://httpbin.org/post
x-ms-blob-type: BlockBlob

{{
'

string,username,password,filename,datetime
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}
{{string}},{{username}},{{password}},{{filename}},{{datetime}}

'
| myfile("batchfile.log")
}}
```  

##### POST XML

```
POST https://httpbin.org/post
Content-Type: application/xml

{
<note>
    <to>{{ username }}</to>
    <from>{{ username }}</from>
    <heading>{{ 'Reminder' | mutate }}</heading>
    <body>{{ 'Don't forget me this weekend!' | mutate }}</body>
</note>
}
```

##### POST JSON  

```
POST https://httpbin.org/post
Content-Type: application/json

{
    "name": "john doe",
    "info": {{ 'this custom input will be mutated by fuzzie' | mutate }}
}
```  

##### GraphQL  

```
POST https://spacex-production.up.railway.app/
X-REQUEST-TYPE: GraphQL

{
    launchesPast(limit: 10) {
      mission_name
      launch_date_local
      launch_site {
        site_name_long
      }
      links {
        article_link
        video_link
      }
      rocket {
        rocket_name
      }
    }
  }
```








    
