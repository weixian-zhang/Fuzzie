from pathlib import Path
import unittest
from openapi3_discoverer import OpenApi3ApiDiscover
from apicontext_model import GetApi, MutatorApi
import os
from pathlib import Path

projectDirPath = os.path.dirname(Path(__file__))

class TestOpenApi3ApiDiscover(unittest.TestCase):
    
    def test_openapi3_get_params_path_object_yaml(self):
        
        apiFilePath = os.path.join(projectDirPath, 'testdata\\testdata-openapi3-get-params-path-object.yaml') 
    
        openapi3 = OpenApi3ApiDiscover()
        
        apicontext = openapi3.load_openapi3_file(apiFilePath)
        
        self.assertTrue(apicontext is not None)
        
        self.assertTrue(len(apicontext.apis) == 1)
        
        api = apicontext.apis[0]
        
        self.assertTrue(len(api.parameters) == 3)
        
        paramProp1 = api.parameters[0]
        paramProp2 = api.parameters[1]
        paramProp3 = api.parameters[2]
        
        
        self.assertEqual(paramProp1.getApiParamIn, 'path')
        self.assertEqual(paramProp1.propertyName, 'complexObject')
        self.assertEqual(paramProp1.parameters[0].propertyName ,'foo')
        self.assertEqual(paramProp1.parameters[0].type , 'string')
        self.assertEqual(paramProp1.parameters[1].propertyName, 'color')
        self.assertEqual(paramProp1.parameters[1].type, 'string')
        
        self.assertEqual(paramProp2.getApiParamIn, 'path')
        self.assertEqual(paramProp2.propertyName, 'doubleParam')
        self.assertEqual(paramProp2.type , 'array')
        self.assertEqual(paramProp2.arrayProp.type, 'integer')
        
        self.assertEqual(paramProp3.getApiParamIn, 'path')
        self.assertEqual(paramProp3.propertyName, 'singleArray')
        self.assertEqual(paramProp3.type , 'array')
        self.assertEqual(paramProp3.arrayProp.type, 'string')
        
        
    
    # def get_nested_parameters(self, api) -> dict:
    #     dict = {}
        
    #     for p in api.parameters:
            
    #         if p.type is not 'object':
    #             dict[p.name] = p.type
    #         elif p.type == 'object':
    #              dict[p.name] = self.get_nested_parameters_handler(p.parameters, {})
            
    
    # def get_nested_parameters_handler(self, parameters, dict):
        
    #     if paramProp is None:
    #         return dict
        
    #     for p in paramProp.parameters:
            
    #         if p.type == 'object':
                
    #             innerParam = p.parameters
    #             while innerParam is not None:
                    
                    
    #         dict[p.name] = p.type
            
        
            
    #     return dict
    


if __name__ == '__main__':
    unittest.main()