## Fuzzie (work in progress)  

Fuzzie is a Rest API fuzz testing tool available first as a VSCode extension, later in the roadmap it will be made available as a command-line tool and also an Azure DevOps Task. These Fuzzie clients provides flexibility to insert Fuzzie in different SDLC stages.  

### How Fuzzie Works  

Fuzzie needs to know the schema of your API so that it can generate inputs to invoke them. There are several ways for Fuzzie to discover your API schemas
* Url to [OpenAPI 3](https://editor.swagger.io/) specification
* File path to OpenAPI 3 specification
* Request-Text (inspired by [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) by Huachao Mao)
  * Input a single Request-Text in VSCode to instruct Fuzzie to fuzz test a single API
  * File path to a list of Request-Texts in a text file e.g: request-texts.fuzzie
  * Supported data types
    * string
    * integer
    * float
    * datetime
    * [username](https://github.com/danielmiessler/SecLists) - common and cracked user names from SecList
    * [password](https://github.com/danielmiessler/SecLists) - common and hacked passwords from SecList

  Examples: 
  <br/>
  <br/>
  
  * single Post Request-Text with OAuth bearer token
    ```
    POST https://example.com/comments HTTP/1.1
    content-type: application/json
    Authorization: Bearer AbCdEf123456
    {
        "name": {{string}},
        "time": {{datetime}}
    }
    ```
  
  * Single GET Querystring Request-Text and one POST Request-Text  
  
    ```
    GET https://httpbin.org/get
     ?name={{string}}&startDate={{datetime}}&endDate={{datetime}}
    content-type: application/json
    Authorization: Basic base64|username:password
    ```
