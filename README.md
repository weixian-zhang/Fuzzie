## Fuzzie (in development)  

Fuzzie is a Rest API fuzz testing tool available as VSCode extension.  
The ability to fuzz test your freshly made APIs right in the IDE brings about several advantages:

* fuzz tests as easy as running unit tests
* the ability to fuzz test very early in the SDLC rather than waiting for feedbacks later in SDLC
* fuzzing tool becomes a <i>personal tool</i> and developers can fuzz test any one or more API at any time and convenience

<img src="https://user-images.githubusercontent.com/43234101/184052538-5770d77e-6872-426a-ac28-cd79161790c6.png" width="600px" height="200" />

<br />

### Software Architecture Design  
*subjected to change, diagram from another hobby project [Azure Workbench](https://www.azureworkbench.com/?id=IsxyrPUWclTXMoDPuAtK)
![image](https://user-images.githubusercontent.com/43234101/188535919-0fb971e1-b68e-47de-8a8a-5c2a461ea1cc.png)  





### Roadmap  
* HTML WebForm fuzzing


### How Fuzzie Works  

Fuzzie needs to know the schema of your APIs so that it understands the parameters in order to generate data to invoke them.  
There are several ways for Fuzzie to discover your API schemas
* Url to [OpenAPI 3](https://editor.swagger.io/) specification
* File path to OpenAPI 3 specification
* Request-Message (inspired from [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) by Huachao Mao)
  * Input a single Request-Message in VSCode to instruct Fuzzie to fuzz test a single API
  * File path to a list of Request-Messages in text file e.g: request-messages.fuzzie
  * supports unlimited request-messages in a single file
  * You can use the following supported data types as case-sensitive variables in Request-Message
  
    * string - courtesy from [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings) and [SecList](https://github.com/danielmiessler/SecLists)
    * integer
    * float
    * datetime
    * [payload](https://github.com/danielmiessler/SecLists) - naughty files, images and zip bombs from SecList
    * [username](https://github.com/danielmiessler/SecLists) - common and cracked user names from SecList
    * [password](https://github.com/danielmiessler/SecLists) - common and hacked passwords from SecList
    
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
    
    
