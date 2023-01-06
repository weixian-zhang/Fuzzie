## Fuzzie (still in development, coming very soon)  

Fuzzie is a simple Rest API and GraphQL fuzzing tool available as VSCode extension.  
The ability to fuzz test your Web APIs and GraphQL APIs directly in the IDE brings about several advantages:

* fuzz tests made simple guided by an intuitive WebView in VSCode
* the ability to fuzz test very early in the SDLC
* Fuzzer in IDE allows developers to conveniently fuzz test anytime without prior knowledge of fuzzing

<br />

### How Fuzzie Works  

Fuzzie VSCode extension comes with a webview everything from API or GraphQL Discovery, fuzzing to analyzing fuzz test result can be done within this webview.
<br />  

#### API Discovery  

Fuzzie needs to know the schema of your APIs, there are 2 ways for Fuzzie to discover your API:
* [OpenAPI 3](https://editor.swagger.io/) specification
  * HTTP Url
  * File path
  
* Request Message (concept inspired by [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) by Huachao Mao)
  * single Request Message or as many Request Messages as you need to fuzz test
  * Text files that contains a list of Request-Messages with extension .http, .rest or .fuzzie
 
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
    
