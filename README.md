## Fuzzie  

Fuzzie is a Rest API fuzz testing tool available first as a VSCode extension, later in the roadmap it will be made available as a command-line tool and also an Azure DevOps Task. These Fuzzie clients provides flexibility to insert Fuzzie in different SDLC stages.  

### How Fuzzie Works  

Fuzzie needs to know the schema of your API so that it can generate inputs to invoke them. There are several ways for Fuzzie to discover your API schemas
* Url to [OpenAPI 3](https://editor.swagger.io/) specification
* File path to OpenAPI 3 specification
* Request-Text
  * Input a single Request-Text in VSCode to instruct Fuzzie to fuzz test a single API
  * File path to a list of Request-Text in a text file e.g: request-text.fuzzie

  Examples: 
  <br/>
  Single Post Request-Text
  POST https://example.com/comments HTTP/1.1
  content-type: application/json

  {
      "name": "sample",
      "time": "Wed, 21 Oct 2015 18:27:50 GMT"
  }
