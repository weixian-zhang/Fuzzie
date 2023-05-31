# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Roadmap] (Date TBD)

### Added  

* New wordlist <b>iterate</b> for iterating a supplied list of primitive typed values.  
E.g: {{ ["Eve", "Alice", "Bob"] | iterate }}

* Fuzz message brokers like Kafka, Azure Service Bus and Azure Event Hub with a new kind of Fuzz Context and domain-specific-language similar to HTTP Request Message but for describing Message-Broker-Message

<br />  

## [ 0.16.0 ] - 2023-05-31  
### Changed
 * Startup time is significantly improved
 * fixed a bug on during parsing Request Message where a line contains ### for e.g: '// some text with triple ###'.  
 Before this fix such a line will not be treated as a comment.

 <br />  

## [ 0.15.0 ] - 2023-04-30  

### Added

Support declaring Variables to be used in request messages.  
E.g  
```
{% set url = 'https://httpbin.org' %}
{% set name = 'Kean' %}
{% set address = '182 Cecil St, #13-01 069547' %}

GET {{ url }}/get
?name={{ name }}
&address={{ address }}
Content-Type: application/xml
Authorization: {{ string }}
CustomHeader-1: {{ digit }}
CustomHeader-2: {{ filename }}
CustomHeader-3: {{ username }}
```
