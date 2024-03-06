## Fuzzie
[<img src="https://badgen.net/badge/vs-marketplace/0.16.0-preview/green" />](https://marketplace.visualstudio.com/items?itemName=wxz.wxz-fuzzie)

Fuzzie is a simple grey-box fuzz testing tool available as VSCode extension for fuzz testing REST API and GraphQL.  
The ability to fuzz test right in VSCode brings about several benefits:

* As early as while debugging APIs in VSCode running on localhost, you can concurrently use Fuzzie to fuzz test your APIs.  
  As Fuzzie also sends random unpredictable data, you can catch common erros from unhandled input parameters early.
* fuzz tests guided by an intuitive WebView
* able to fuzz test any parts of a HTTP message by creating your request messages with built-in wordlist, functions and variables
* Being available in VSCode allows developers to conveniently fuzz test anytime without prior knowledge of fuzzing

## What Information Does Fuzzie Collects?

* Fuzzie does not collect personal data
* Fuzzie collects all HTTP Request and Response related data of the user's specified test-target Web APIs and Websites.
  If authentication tokens and keys are supplied to Fuzzie to be able to authenticate itself to the targetted Web APIs and Websites, Fuzzie stores these authentication tokens and keys.
  All data including authentication token, keys, HTTP request and response collected, are stored locally within VSCode extension folder. The data is not send over to any remote servers.
 

### *Things to Note    

* Depending on [wordlist type](#2-write-http-request-messages), Fuzzie can send malicious strings from [SecList](https://github.com/danielmiessler/SecLists), recommend to use Fuzzie in test environments only
* requires Python 3.10 and above
* Fuzzie uses port 50001  
  fuzzer engine listens on http://localhost:50001 serving requests from webview
* Fuzzie uses sqlite internally to store all data, when upgrading to a newer extension version, previous data will not be retained
* On VSCode first launch, Fuzzie can take up to 7-9 secs to start up

<br />  

### Content  
* [Launching Fuzzie](#launching-fuzzie)
* [Using Fuzzie](#using-fuzzie )
* [How to write HTTP Request Message ](#2-writing-http-request-messages)  
  * [Variable](#variables)
  * [Wordlist Types](#wordlist-types)
  * [Functions](#functions)
* [More examples of Request Messages](#21-request-message-examples)

<br /> 

### Launching Fuzzie  

Open VSCode command palette (Ctrl + Shift + P) and search for "Fuzzie"  
<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/how%20to%20launch%20fuzzie.png" />


### Using Fuzzie 

Fuzzie VSCode extension provides a webview for you to perform everything from writing request messages to discover API and GraphQL, to fuzzing and analyzing test result, all in a single place.  

<br /> 

![Animation - Copy](https://github.com/weixian-zhang/Fuzzie/blob/main/doc/fuzzie-webview-walkthrough.gif)

<br />  

#### 1. Webview Navigation  

<img src ="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/tutorial-fuzzie-webview.png" />

#### 2. Start by creating a  new API Fuzz Context

A Fuzz Context contains a list of cohesive "test cases" created by writing [HTTP Request Messages](#http-write-request-messages).  
Each test case contains HTTP verb, domain name, port, path, querystring, headers and body and Fuzzie make HTTP requests against all test cases in a Fuzz Context. 

<img src="https://github.com/weixian-zhang/Fuzzie/blob/main/doc/tutorial/create-new-api-context.png" />  

#### 2. Writing HTTP Request Messages  

Your REST and GraphQL target endpoints are described by writing Request Messages.  
The concept of Request Message is fully inspired by [Hau Chao's VSCode Rest Client project](https://github.com/Huachao/vscode-restclient#select-request-text).  

```
//this is a comment
# and this is comment too

{VERB} {url}
{headers}

{body}
```

In a request message, you can <b>replace any part of path, querystring, header, body with Fuzzie's [Wordlists or Functions](#wordlist-types)</b>.  
By replacing parameter with {{ wordlist type }} , during fuzzing, Fuzzie will replace the wordlist with fuzz data depending on the type of wordlist.  
  * wordlist type = fuzz data type e.g: sql-inection string, xss string, hacked usernames and password and more
  * function = transform, iterate or randomize your provided input
for example:

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

{{ wordlist type }} will be replaced with fuzz data during fuzzing  
```
GET https://httpbin.org:443/get?name=!root&address=undefined&order=5&mode=select user from sysibm.sysdummy1;

Content-Type:application/xml
Authorization:IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1))/*'XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR'|XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),âSLEEP(1)))OR*/
CustomHeader-1:-£100000
CustomHeader-2:HRUZgKCQcM7deZue.class
CustomHeader-3:$ALOC$
User-Agent:fuzzie
```

### Variables  

starting at version 0.15-preview, Fuzzie supports Variables  

```
{% set url = 'https://httpbin.org' %}
{% set name = 'Kean' %}
{% set address = '182 Cecil St, #13-01 069547' %}

###

GET {{ url }}/get
?name={{ name }}
&address={{ address }}
Content-Type: application/xml
Authorization: {{ string }}
CustomHeader-1: {{ digit }}
CustomHeader-2: {{ filename }}
CustomHeader-3: {{ username }}

```

Edit variables in API Context  
![image](https://user-images.githubusercontent.com/43234101/235344075-ce5a921e-3945-44d6-a644-6639eea5e5db.png)

### Wordlist Types
The following are built-in wordlist-types, more will be added in future  
Type = wordlist provides data  
Type = function acts on your provided custom data
| WordList Type | Is Primitive wordlist type | file upload | Description |
| ------------- |-------------| -------------| ------------- |
| {{ string }} |  yes | no | naughty strings from [minimaxir/big-list-of-naughty-strings](https://github.com/minimaxir/big-list-of-naughty-strings) | 
| {{ xss }} | yes | no | cross-site scripting strings from [danielmiessle/seclist](https://github.com/danielmiessler/SecLists) |
| {{ sqlinject }} | yes | no | sql-injection strings from danielmiessle/seclist |
| {{ bool }} | yes | no | boolean values and something naughty |
| {{ digit }} | yes | no | Integers, floats and something naughty |
| {{ char }} | yes | no | naughty chars |
| {{ image }} |  no | yes | DALL-E images and a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist | 
| {{ pdf }} |  no | yes | Fuzzie generated fake PDF with a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist |
| {{ file }} |  no | yes | naughty [payload](https://github.com/danielmiessler/SecLists/tree/master/Payloads) from danielmiessle/seclist |
| <br>{{<br> '<br>custom file content<br>'<br> &#124; myfile('filename.csv')<br> }} | no | yes | Custom file content within single quite '...' are uploaded as file<br>{{<br>'<br>this is a file content<br>{{string}} {{username}}<br>'<br> &#124; myfile("data.json")<br>}}  |
| {{ datetime }} | yes | no | date + time | 
| {{ date }} | yes | no | date only |
| {{ time }} | yes | no | time only |
| {{ username }} | yes | no | hacked [usernames](https://github.com/danielmiessler/SecLists/tree/master/Usernames) from danielmiessler seclist |
| {{ password }} | yes | no | hacked [password](https://github.com/danielmiessler/SecLists/tree/master/Passwords) from danielmiessler seclist 
| {{ filename }} | yes | no | random file name and extensions |  wordlist |
| {{ httppath }} | yes | no | discover [directories and files](https://github.com/danielmiessler/SecLists/tree/master/Discovery) from danielmiessler seclist |

### Functions  

| WordList Type | Description |
| ------------- |-------------|
| {{ numrange(start, end) }} | increment number by 1 from start to end. <br>Example numrange(1, 5000): result is 1, 2, 3,...4999, 5000 |
| {{ 'a quick brown fox' &#124; <b>mutate</b> }} | input will be mutated |
| {{ ['a', 'list', 'of', 'items' ]  &#124; <b>random</b> }} | returns a random item from your list |
| {{ <br>'single string to be base64 encoded' &#124; <b>base64e</b> }}<br> <br>{{ ['list', 'of', 'items', 'to be base64 encoded'] &#124; <b>base64e</b> }}<br>  | base64 encodes your input, or if a list is supplied, randomly pick an item and encodes it |
| {{ <br>'base64 encoded string to be decoded' &#124; <b>base64d</b> }}<br> <br>{{ ['list', 'of', 'encoded', 'items', 'to be base64 decoded'] &#124; <b>base64d</b> }}<br>  | base64 encodes your input, or if a list is supplied, randomly pick an item and encodes it |

<br> 


#### 2.1 Request Message Examples  

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








    
