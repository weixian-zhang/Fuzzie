## Fuzzie  

Fuzzie is a Rest API fuzz testing tool available first as a VSCode extension, later in the roadmap it will be made available as a command-line tool and also an Azure DevOps Task. These Fuzzie clients provides flexibility to insert Fuzzie in different SDLC stages.  

### How Fuzzie Works  

Fuzzie needs to know the schema of your API so that it can generate inputs to invoke them. There are several ways for Fuzzie to discover your API schemas
* Url to [OpenAPI 3](https://editor.swagger.io/) document specification
* File path to 
