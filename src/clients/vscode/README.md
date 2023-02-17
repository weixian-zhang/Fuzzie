## Fuzzie
<img src="https://badgen.net/badge/version/1.0.0-alpha/green" />

Fuzzie is a simple grey-box fuzz testing tool available as VSCode extension for fuzz testing REST API and GraphQL.  
The ability to fuzz test your REST and GraphQL APIs directly in an IDE brings about several advantages:

* fuzz tests guided by an intuitive WebView
* the ability to fuzz test very early during software development
* Being available in VSCode allows developers to conveniently fuzz test anytime without prior knowledge of fuzzing

### *Things to Note    

* requires Python 3.10 and above
* Fuzzie uses port 50001  
  fuzzer engine listens on http://localhost:50001 serving requests from webview
* Fuzzie uses sqlite internally to store all data, when upgrading to a newer extension version, previous data will not be retained

### Launching Fuzzie  

Open VSCode command palette (Ctrl + Shift + P) and search for "Fuzzie"  
<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/how%20to%20launch%20fuzzie.png" />


### Using Fuzzie 

Fuzzie VSCode extension provides a webview for you to perform everything from API and GraphQL discovery to fuzzing and analyzing test result, all in a single place.  

<br /> 

![Animation - Copy](https://user-images.githubusercontent.com/43234101/211010226-679c7e24-50a6-4a64-ad32-8fd3e40642fe.gif)

<br />  

#### 1. Webview Navigation  

<img src ="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/tutorial-fuzzie-webview.png" />

#### 2. Start by creating a  new API Fuzz Context

A Fuzz Context contains a list of cohesive "fuzz test cases" created by writing [HTTP Request Messages](#http-write-request-messages).  
Each test case contains HTTP verb, domain name, port, path, querystring, headers and body and Fuzzie make HTTP requests against all test cases in a Fuzz Context. 

<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/create-new-api-context.png" />  

#### 2. Write HTTP Request Messages  

Your REST and GraphQL contracts are described by writing Request Messages.  
The concept of Request Message is fully inspired by [Hau Chao's VSCode Rest Client project](https://github.com/Huachao/vscode-restclient#select-request-text).  

In request message, you can replace any parameter in path, querystring, header, body with Fuzzie's built-in [Wordlists](#wordlist-types).  
By replacing parameter with wordlist {{ wordlist type }}, during fuzzing, Fuzzie will replace the wordlist with fuzz data depending on the type of wordlist.

#### Wordlist Types
The following are built-in wordlist-types, more will be added in future  
| WordList Type | Is Primitive wordlist type | file upload | Description   |
| ------------- |-------------| -------------| ------------- |
| {{ 'a quick brown fox' &#124; mutate }} | yes | no | your custom input that Fuzzie mutates |
| {{ string }} |  yes | no | naughty strings from [minimaxir/big-list-of-naughty-strings](https://github.com/minimaxir/big-list-of-naughty-strings) |
| {{ xss }} | yes | no | cross-site scripting strings from [danielmiessle/seclist](https://github.com/danielmiessler/SecLists) |
| {{ sqlinject }} | yes | no | sql-injection strings from danielmiessle/seclist |
| {{ bool }} | yes | no | boolean values and something naughty |
| {{ digit }} | yes | no | Integers, floats and something naughty |
| {{ char }} | yes | no | naughty chars |
| {{ image }} |  no | yes | DALL-E images and a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist |
| {{ pdf }} |  no | yes | Fuzzie generated fake PDF with a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist |
| {{ file }} |  no | yes | naught payload from danielmiessle/seclist |
| <br>{{<br> '<br>custom file content<br>'<br> &#124; myfile('filename.csv')<br> }} | no | yes | Custom file content within single quite '...' are uploaded as file<br>{{<br>'<br>this is a file content<br>{{string}} {{username}}<br>'<br> &#124; myfile("data.json")<br>}}  |
| {{ datetime }} | yes | no | date + time |
| {{ date }} | yes | no | date only |
| {{ time }} | yes | no | time only |
| {{ username }} | yes | no | hacked usernames from danielmiessler seclist |
| {{ password }} | yes | no | hacked password from danielmiessler seclist |
| {{ filename }} | yes | no | random file name and extensions |  

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








    
