# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - date TBD

### Added  

New wordlist {{ iterate }} to iterate a supplied list of primitive typed values.  
E.g: {{ ["Eve", "Alice", "Bob"] | iterate }}
  

## v0.15 - 2023-04-30  

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
