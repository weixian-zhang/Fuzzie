## Fuzzie (coming soon)  

Fuzzie is a simple Rest API and GraphQL fuzzing tool available as VSCode extension.  
The ability to fuzz test your Web APIs and GraphQL APIs directly in the IDE brings about several advantages:

* fuzz tests guided by an intuitive WebView
* the ability to fuzz test very early in the SDLC
* Fuzzer in IDE allows developers to conveniently fuzz test anytime without prior knowledge of fuzzing

<br />

### Prerequisites    

Fuzzie requires Python 3.10 and above

### Launching Fuzzie  

Open VSCode command palette (Ctrl + Shift + P) and search for "Fuzzie"


### How Fuzzie Works  

Fuzzie VSCode extension comes with a webview, everything from API and GraphQL discovery to fuzzing and analyzing test result can be done in webview.  

![Animation - Copy](https://user-images.githubusercontent.com/43234101/211010226-679c7e24-50a6-4a64-ad32-8fd3e40642fe.gif)

<br />  

#### Terms and Concepts

* Fuzz Context - fuzz context contains hostname, port, number of test cases to fuzz, and API operations discovered by writing Request Messages
* wordlist-type - the real potential of Fuzzie is allowing user to write [Request Messages](#api-discovery) and Fuzzie converts each Request Message into a http call.  Within Request Message, exact input format like JSON, XML, files, plain text or simply any format, with parameters can be described in Request Message.
By replacing wordlist-type {{ wordlist type }} with parameter value, during fuzzing, Fuzzie will replace the parameter values with fuzz data, thus, performing a Grey-Box testing on your REST and GraphQL APIs.  
example:  

```
POST https://httpbin.org/post  

{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}
```  

```
POST https://httpbin.org/post 

{
    "glossary": {
        "title": "{{ string }}",
		"GlossDiv": {
            "title": "{{ string }}",
			"GlossList": {
                "GlossEntry": {
                    "ID": "{{ digit }}",
					"SortAs": "{{ string }}",
					"GlossTerm": "{{ "Standard Generalized Markup Language" | my }}",
					"Acronym": "{{ string }}",
					"Abbrev": "ISO {{ digit }}:{{ digit }}",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["{{ "GML" | my }}", "{{ "XML" | my }}"]
                    },
					"GlossSee": "{{ string }}"
                }
            }
        }
    }
}
```  

The following are built-in wordlist-types available today, more will be added in future  
| WordList Type | Description   |
| ------------- |:-------------:| 
| {{ 'a quick brown fox' &#124; mutate }} | your custom input, Fuzzie will mutate your input |
| {{ string }} | naughty string from [minimaxir/big-list-of-naughty-strings](https://github.com/minimaxir/big-list-of-naughty-strings) |
| {{ xss }} | cross-site scripting strings from [danielmiessle/seclist](https://github.com/danielmiessler/SecLists) |
| {{ sqlinject }} | sql-injection string from danielmiessle/seclist |
| {{ bool }} | boolean values and something naughty |
| {{ digit }} | Integers, floats and something naughty |
| {{ char }} | naughty chars |
| {{ image }} |  DALL-E images and a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist |
| {{ pdf }} |  Fuzzie generated fake PDF with a mix of naughty payloads (same as {{ file }} ) from danielmiessle/seclist |
| {{ file }} |  naught payload from danielmiessle/seclist |
| {{ datetime }} | date + time |
| {{ date }} | date only |
| {{ time }} | time only |
| {{ username }} | hacked usernames from danielmiessler seclist |
| {{ password }} | hacked password from danielmiessler seclist |
| {{ filename }} | random file name and extensions |


</ br>
#### API Discovery  

Fuzzie needs to know your API or GraphQL "schema", this is achieved by Request Messages (concept inspired by [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) by Huachao Mao)

  * write Request Message(s) in webview while creating a new Fuzz Context
  * Fuzzie takes in text files that contains Request-Messages with file extension .http, .rest or .fuzzie
 
 Request Message can be written and validated in webview provided by Fuzzie  
 
 ![image](https://user-images.githubusercontent.com/43234101/210977019-4b671b68-99e1-455b-bc8b-8fc147440140.png)  
 
 <br />
 
 ![image](https://user-images.githubusercontent.com/43234101/210977575-54ce66aa-2e0b-4b9a-b914-d47e0995c701.png)


    
  <br/>
  Examples: 
  <br/>
 
  * Post Request-Message, OAuth bearer token and Json body
    ```
    POST https://example.com/comments HTTP/1.1
    content-type: application/json
    Authorization: Bearer AbCdEf123456
    
    {
        "name": {{string}},
        "time": {{datetime}}
    }
    ```
  
  * GET Request-Message, fuzzing querystring parameters, username and password
  
    ```
    GET https://httpbin.org/get
     ?name={{string}}
     &startDate={{datetime}}
     &endDate={{datetime}}
     
    content-type: application/json
    Authorization: Basic base64|{{username}}:{{password}}
    ```
  * GET Request-Message, fuzzing path parameters, username and password
  
    ```
    GET https://httpbin.org/get/{{string}}/{{datetime}}/{{datetime}}
     
    content-type: application/json
    Authorization: Basic base64|{{username}}:{{password}}
    ```
    
  * POST multipart-form from example HTML
    ```
    <!DOCTYPE html>
     <html lang="en">
     <head>
       <meta charset="utf-8"/>
       <title>upload</title>
     </head>
     <body>
     <form action="http://localhost:8000" method="post" enctype="multipart/form-data">
       <p><input type="text" name="text1" value="text default">
       <p><input type="text" name="text2" value="a&#x03C9;b">
       <p><input type="file" name="file1">
       <p><input type="file" name="file2">
       <p><input type="file" name="file3">
       <p><button type="submit">Submit</button>
     </form>
     </body>
     </html>     
    ```  
    ```
    POST https://api.contoso.com/order/upload
    Content-Type: multipart/form-data; boundary=---------------------------735323031399963166993862150
    Content-Length: 834

    -----------------------------735323031399963166993862150
    Content-Disposition: form-data; name="text1"

    {{string}}
    -----------------------------735323031399963166993862150
    Content-Disposition: form-data; name="text2"

    {{string}}
    -----------------------------735323031399963166993862150
    Content-Disposition: form-data; name="file1"; filename="a.txt"
    Content-Type: text/plain

    {{payload}}

    -----------------------------735323031399963166993862150
    Content-Disposition: form-data; name="file2"; filename="a.html"
    Content-Type: text/html

    {{payload}}

    -----------------------------735323031399963166993862150
    Content-Disposition: form-data; name="file3"; filename="binary"
    Content-Type: application/octet-stream

    {{payload}}
    ```
    
    ### Software Architecture Design  
*subjected to change, diagram from another hobby project [Azure Workbench](https://www.azureworkbench.com/?id=IsxyrPUWclTXMoDPuAtK)
![image](https://user-images.githubusercontent.com/43234101/188535919-0fb971e1-b68e-47de-8a8a-5c2a461ea1cc.png)  
    
