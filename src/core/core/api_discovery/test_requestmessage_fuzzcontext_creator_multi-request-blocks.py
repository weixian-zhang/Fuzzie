import unittest
import base64
import os
import sys
from pathlib import Path

projectDirPath = os.path.dirname(Path(__file__))
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)

sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from models.webapi_fuzzcontext import SupportedAuthnType
from utils import Utils
from webapi_fuzzcontext import ApiFuzzCaseSet, ApiFuzzContext
from requestmessage_fuzzcontext_creator import RequestMessageFuzzContextCreator

class TestRequestMessageFuzzContextCreator_By_MultiBlocks(unittest.TestCase):
    
# parsing body with
    #     multiple comments
    #     multiple request-block delimiter
    #     no headers
    #     multiple breaklines between requestline and body
    #     multiple files
    #     json 
    #     multiple breaklines between header and body
    def test_reqmsg_parser_body_no_header_breakline_multiple_files_complex_json(self):
            
        
            rq = '''

            
            POST https://example.com/user?name={{username}}&address={{string}}
            Content-Type: application/xml
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
            
            
            {{ file   }}
                
                {{ pdf   }}
                
                {{ image   }}
                
                
                {
                "id": "0001",
                "type": "{{string}}",
                "name": "{{string}}",
                "ppu": {{digit}},
                "batters":
                    {
                        "batter":
                            [
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" }
                            ]
                    },
                "topping":
                    [
                        { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
                        { "id": "5002", "name": "{{ my:[Glazed] }}" },
                        { "id": "5005", "name": "{{ my:[Sugar] }}" },
                    ]
            }
                
                {{ pdf   }}
                
                # going into another secton
                
                ###
                
                #this is a comment
                
                https://example.com/user/1
                
                ###
                
                #this is a comment
                
                https://example.com/user/1
                
                
                
                ###
                
                
                
                POST https://example.com/user?name={{username}}&address={{string}}
            Content-Type: application/xml
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
            
            
            {{ file   }}
                
                {{ pdf   }}
                
                {{ image   }}
                
                
                {
                "id": "0001",
                "type": "{{string}}",
                "name": "{{string}}",
                "ppu": {{digit}},
                "batters":
                    {
                        "batter":
                            [
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" }
                            ]
                    },
                "topping":
                    [
                        { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
                        { "id": "5002", "name": "{{ my:[Glazed] }}" },
                        { "id": "5005", "name": "{{ my:[Sugar] }}" },
                    ]
            }
                
            
            '''
            
            rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
            
            rqMsgFCCreator = RequestMessageFuzzContextCreator()
            
            ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                                apiDiscoveryMethod= "request_message",
                                name= "request-message-test",
                                hostname='https://example.com',
                                port='443',
                                authnType=SupportedAuthnType.Anonymous.name,
                                fuzzcaseToExec=500,
                                openapi3FilePath='',
                                requestTextContent= rqB64
                                )
            
            self.assertTrue(ok)
            self.assertTrue(error == '')
            self.assertTrue(len(apicontext.fuzzcaseSets), 2)
            
            # fuzzcaseset 1
            self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
            self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
        
            self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 4)
            
            # fuzzcaseset 2
            self.assertTrue(apicontext.fuzzcaseSets[1].verb == 'GET')
            self.assertTrue(apicontext.fuzzcaseSets[1].path == '/user/1')
            
            # fuzzcaseset 3
            self.assertTrue(apicontext.fuzzcaseSets[2].verb == 'GET')
            self.assertTrue(apicontext.fuzzcaseSets[2].path == '/user/1')
            
            # fuzzcaseset 4
            self.assertTrue(apicontext.fuzzcaseSets[3].headerNonTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[3].headerDataTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[3].bodyNonTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
            self.assertTrue(apicontext.fuzzcaseSets[3].bodyDataTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
            
    
    # parsing body with
    #     multiple comments
    #     multiple empty sections
    #     multiple request-block delimiter
    #     no headers
    #     multiple breaklines between requestline and body
    #     multiple files
    #     json 
    #     multiple breaklines between header and body
    def test_reqmsg_parser_body_no_header_breakline_multiple_files_complex_json(self):
            
        
            rq = '''

            
            POST https://example.com/user?name={{username}}&address={{string}}
            Content-Type: application/xml
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
            
            
            {{ file   }}
                
                {{ pdf   }}
                
                {{ image   }}
                
                
                {
                "id": "0001",
                "type": "{{string}}",
                "name": "{{string}}",
                "ppu": {{digit}},
                "batters":
                    {
                        "batter":
                            [
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" }
                            ]
                    },
                "topping":
                    [
                        { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
                        { "id": "5002", "name": "{{ my:[Glazed] }}" },
                        { "id": "5005", "name": "{{ my:[Sugar] }}" },
                    ]
            }
                
                {{ pdf   }}
                
                # going into another secton
                
                ###
                
                #this is a comment
                
                https://example.com/user/1
                
                ###
                
                #this is a comment
                
                https://example.com/user/1
                
                
                
                ###
                
                
                
                POST https://example.com/user?name={{username}}&address={{string}}
            Content-Type: application/xml
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
            
            
            {{ file   }}
                
                {{ pdf   }}
                
                {{ image   }}
                
                
                {
                "id": "0001",
                "type": "{{string}}",
                "name": "{{string}}",
                "ppu": {{digit}},
                "batters":
                    {
                        "batter":
                            [
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" },
                                { "id": "{{digit}}", "type": "{{string}}" }
                            ]
                    },
                "topping":
                    [
                        { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
                        { "id": "5002", "name": "{{ my:[Glazed] }}" },
                        { "id": "5005", "name": "{{ my:[Sugar] }}" },
                    ]
            }
            
            
            
            
            
            ###
            
            # empty section
            ###
            
            # more empty section
            
            ###
            
            POST https://example.com/user?name={{username}}&address={{string}}
            Content-Type: application/xml
            
            
            
            
            {{ file   }}
                
                {{ pdf   }}
                
                {{ image   }}
                
                
                <?xml version="1.0"?>
                    <catalog>
                    <book id="bk101">
                        <author>Gambardella, Matthew</author>
                        <title>XML Developer's Guide</title>
                        <genre>Computer</genre>
                        <price>44.95</price>
                        <publish_date>2000-10-01</publish_date>
                        <description>An in-depth look at creating applications 
                        with XML.</description>
                    </book>
                    <book id="bk102">
                        <author>Ralls, Kim</author>
                        <title>Midnight Rain</title>
                        <genre>Fantasy</genre>
                        <price>5.95</price>
                        <publish_date>2000-12-16</publish_date>
                        <description>A former architect battles corporate zombies, 
                        an evil sorceress, and her own childhood to become queen 
                        of the world.</description>
                    </book>
                    <book id="bk103">
                        <author>Corets, Eva</author>
                        <title>Maeve Ascendant</title>
                        <genre>Fantasy</genre>
                        <price>5.95</price>
                        <publish_date>2000-11-17</publish_date>
                        <description>After the collapse of a nanotechnology 
                        society in England, the young survivors lay the 
                        foundation for a new society.</description>
                    </book>
                    <book id="bk104">
                        <author>Corets, Eva</author>
                        <title>Oberon's Legacy</title>
                        <genre>Fantasy</genre>
                        <price>5.95</price>
                        <publish_date>2001-03-10</publish_date>
                        <description>In post-apocalypse England, the mysterious 
                        agent known only as Oberon helps to create a new life 
                        for the inhabitants of London. Sequel to Maeve 
                        Ascendant.</description>
                    </book>
                    <book id="bk105">
                        <author>Corets, Eva</author>
                        <title>The Sundered Grail</title>
                        <genre>Fantasy</genre>
                        <price>5.95</price>
                        <publish_date>2001-09-10</publish_date>
                        <description>The two daughters of Maeve, half-sisters, 
                        battle one another for control of England. Sequel to 
                        Oberon's Legacy.</description>
                    </book>
                    <book id="bk106">
                        <author>Randall, Cynthia</author>
                        <title>Lover Birds</title>
                        <genre>Romance</genre>
                        <price>4.95</price>
                        <publish_date>2000-09-02</publish_date>
                        <description>When Carla meets Paul at an ornithology 
                        conference, tempers fly as feathers get ruffled.</description>
                    </book>
                    <book id="bk107">
                        <author>Thurman, Paula</author>
                        <title>Splish Splash</title>
                        <genre>Romance</genre>
                        <price>4.95</price>
                        <publish_date>2000-11-02</publish_date>
                        <description>A deep sea diver finds true love twenty 
                        thousand leagues beneath the sea.</description>
                    </book>
                    <book id="bk108">
                        <author>Knorr, Stefan</author>
                        <title>Creepy Crawlies</title>
                        <genre>Horror</genre>
                        <price>4.95</price>
                        <publish_date>2000-12-06</publish_date>
                        <description>An anthology of horror stories about roaches,
                        centipedes, scorpions  and other insects.</description>
                    </book>
                    <book id="bk109">
                        <author>Kress, Peter</author>
                        <title>Paradox Lost</title>
                        <genre>Science Fiction</genre>
                        <price>6.95</price>
                        <publish_date>2000-11-02</publish_date>
                        <description>After an inadvertant trip through a Heisenberg
                        Uncertainty Device, James Salway discovers the problems 
                        of being quantum.</description>
                    </book>
                    <book id="bk110">
                        <author>O'Brien, Tim</author>
                        <title>Microsoft .NET: The Programming Bible</title>
                        <genre>Computer</genre>
                        <price>36.95</price>
                        <publish_date>2000-12-09</publish_date>
                        <description>Microsoft's .NET initiative is explored in 
                        detail in this deep programmer's reference.</description>
                    </book>
                    <book id="bk111">
                        <author>O'Brien, Tim</author>
                        <title>MSXML3: A Comprehensive Guide</title>
                        <genre>Computer</genre>
                        <price>36.95</price>
                        <publish_date>2000-12-01</publish_date>
                        <description>The Microsoft MSXML3 parser is covered in 
                        detail, with attention to XML DOM interfaces, XSLT processing, 
                        SAX and more.</description>
                    </book>
                    <book id="bk112">
                        <author>Galos, Mike</author>
                        <title>Visual Studio 7: A Comprehensive Guide</title>
                        <genre>Computer</genre>
                        <price>49.95</price>
                        <publish_date>2001-04-16</publish_date>
                        <description>Microsoft Visual Studio 7 is explored in depth,
                        looking at how Visual Basic, Visual C++, C#, and ASP+ are 
                        integrated into a comprehensive development 
                        environment.</description>
                    </book>
                    </catalog>
                
                {{ pdf   }}
                
            
            '''
            
            rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
            
            rqMsgFCCreator = RequestMessageFuzzContextCreator()
            
            ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                                apiDiscoveryMethod= "request_message",
                                name= "request-message-test",
                                hostname='https://example.com',
                                port='443',
                                authnType=SupportedAuthnType.Anonymous.name,
                                fuzzcaseToExec=500,
                                openapi3FilePath='',
                                requestTextContent= rqB64
                                )
            
            self.assertTrue(ok)
            self.assertTrue(error == '')
            self.assertTrue(len(apicontext.fuzzcaseSets), 4)
            
            # fuzzcaseset 1
            self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
            self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
        
            self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 4)
            
            # fuzzcaseset 2
            self.assertTrue(apicontext.fuzzcaseSets[1].verb == 'GET')
            self.assertTrue(apicontext.fuzzcaseSets[1].path == '/user/1')
            
            # fuzzcaseset 3
            self.assertTrue(apicontext.fuzzcaseSets[2].verb == 'GET')
            self.assertTrue(apicontext.fuzzcaseSets[2].path == '/user/1')
            
            # fuzzcaseset 4
            self.assertTrue(apicontext.fuzzcaseSets[3].headerNonTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[3].headerDataTemplate == '{"Content-Type": "application/xml", "Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}"}')
            self.assertTrue(apicontext.fuzzcaseSets[3].bodyNonTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
            self.assertTrue(apicontext.fuzzcaseSets[3].bodyDataTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
            
            # fuzzcaseset 5
            self.assertTrue(len(apicontext.fuzzcaseSets[4].file) == 4)
            self.assertTrue(apicontext.fuzzcaseSets[4].bodyNonTemplate == '<?xml version="1.0"?><catalog><book id="bk101"><author>Gambardella, Matthew</author><title>XML Developer\'s Guide</title><genre>Computer</genre><price>44.95</price><publish_date>2000-10-01</publish_date><description>An in-depth look at creating applicationswith XML.</description></book><book id="bk102"><author>Ralls, Kim</author><title>Midnight Rain</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-12-16</publish_date><description>A former architect battles corporate zombies,an evil sorceress, and her own childhood to become queenof the world.</description></book><book id="bk103"><author>Corets, Eva</author><title>Maeve Ascendant</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-11-17</publish_date><description>After the collapse of a nanotechnologysociety in England, the young survivors lay thefoundation for a new society.</description></book><book id="bk104"><author>Corets, Eva</author><title>Oberon\'s Legacy</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-03-10</publish_date><description>In post-apocalypse England, the mysteriousagent known only as Oberon helps to create a new lifefor the inhabitants of London. Sequel to MaeveAscendant.</description></book><book id="bk105"><author>Corets, Eva</author><title>The Sundered Grail</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-09-10</publish_date><description>The two daughters of Maeve, half-sisters,battle one another for control of England. Sequel toOberon\'s Legacy.</description></book><book id="bk106"><author>Randall, Cynthia</author><title>Lover Birds</title><genre>Romance</genre><price>4.95</price><publish_date>2000-09-02</publish_date><description>When Carla meets Paul at an ornithologyconference, tempers fly as feathers get ruffled.</description></book><book id="bk107"><author>Thurman, Paula</author><title>Splish Splash</title><genre>Romance</genre><price>4.95</price><publish_date>2000-11-02</publish_date><description>A deep sea diver finds true love twentythousand leagues beneath the sea.</description></book><book id="bk108"><author>Knorr, Stefan</author><title>Creepy Crawlies</title><genre>Horror</genre><price>4.95</price><publish_date>2000-12-06</publish_date><description>An anthology of horror stories about roaches,centipedes, scorpions  and other insects.</description></book><book id="bk109"><author>Kress, Peter</author><title>Paradox Lost</title><genre>Science Fiction</genre><price>6.95</price><publish_date>2000-11-02</publish_date><description>After an inadvertant trip through a HeisenbergUncertainty Device, James Salway discovers the problemsof being quantum.</description></book><book id="bk110"><author>O\'Brien, Tim</author><title>Microsoft .NET: The Programming Bible</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-09</publish_date><description>Microsoft\'s .NET initiative is explored indetail in this deep programmer\'s reference.</description></book><book id="bk111"><author>O\'Brien, Tim</author><title>MSXML3: A Comprehensive Guide</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-01</publish_date><description>The Microsoft MSXML3 parser is covered indetail, with attention to XML DOM interfaces, XSLT processing,SAX and more.</description></book><book id="bk112"><author>Galos, Mike</author><title>Visual Studio 7: A Comprehensive Guide</title><genre>Computer</genre><price>49.95</price><publish_date>2001-04-16</publish_date><description>Microsoft Visual Studio 7 is explored in depth,looking at how Visual Basic, Visual C++, C#, and ASP+ areintegrated into a comprehensive developmentenvironment.</description></book></catalog>')
            self.assertTrue(apicontext.fuzzcaseSets[4].bodyDataTemplate == '<?xml version="1.0"?><catalog><book id="bk101"><author>Gambardella, Matthew</author><title>XML Developer\'s Guide</title><genre>Computer</genre><price>44.95</price><publish_date>2000-10-01</publish_date><description>An in-depth look at creating applicationswith XML.</description></book><book id="bk102"><author>Ralls, Kim</author><title>Midnight Rain</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-12-16</publish_date><description>A former architect battles corporate zombies,an evil sorceress, and her own childhood to become queenof the world.</description></book><book id="bk103"><author>Corets, Eva</author><title>Maeve Ascendant</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-11-17</publish_date><description>After the collapse of a nanotechnologysociety in England, the young survivors lay thefoundation for a new society.</description></book><book id="bk104"><author>Corets, Eva</author><title>Oberon\'s Legacy</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-03-10</publish_date><description>In post-apocalypse England, the mysteriousagent known only as Oberon helps to create a new lifefor the inhabitants of London. Sequel to MaeveAscendant.</description></book><book id="bk105"><author>Corets, Eva</author><title>The Sundered Grail</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-09-10</publish_date><description>The two daughters of Maeve, half-sisters,battle one another for control of England. Sequel toOberon\'s Legacy.</description></book><book id="bk106"><author>Randall, Cynthia</author><title>Lover Birds</title><genre>Romance</genre><price>4.95</price><publish_date>2000-09-02</publish_date><description>When Carla meets Paul at an ornithologyconference, tempers fly as feathers get ruffled.</description></book><book id="bk107"><author>Thurman, Paula</author><title>Splish Splash</title><genre>Romance</genre><price>4.95</price><publish_date>2000-11-02</publish_date><description>A deep sea diver finds true love twentythousand leagues beneath the sea.</description></book><book id="bk108"><author>Knorr, Stefan</author><title>Creepy Crawlies</title><genre>Horror</genre><price>4.95</price><publish_date>2000-12-06</publish_date><description>An anthology of horror stories about roaches,centipedes, scorpions  and other insects.</description></book><book id="bk109"><author>Kress, Peter</author><title>Paradox Lost</title><genre>Science Fiction</genre><price>6.95</price><publish_date>2000-11-02</publish_date><description>After an inadvertant trip through a HeisenbergUncertainty Device, James Salway discovers the problemsof being quantum.</description></book><book id="bk110"><author>O\'Brien, Tim</author><title>Microsoft .NET: The Programming Bible</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-09</publish_date><description>Microsoft\'s .NET initiative is explored indetail in this deep programmer\'s reference.</description></book><book id="bk111"><author>O\'Brien, Tim</author><title>MSXML3: A Comprehensive Guide</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-01</publish_date><description>The Microsoft MSXML3 parser is covered indetail, with attention to XML DOM interfaces, XSLT processing,SAX and more.</description></book><book id="bk112"><author>Galos, Mike</author><title>Visual Studio 7: A Comprehensive Guide</title><genre>Computer</genre><price>49.95</price><publish_date>2001-04-16</publish_date><description>Microsoft Visual Studio 7 is explored in depth,looking at how Visual Basic, Visual C++, C#, and ASP+ areintegrated into a comprehensive developmentenvironment.</description></book></catalog>')
            
            
if __name__ == '__main__':
    unittest.main()