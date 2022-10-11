from pathlib import Path
import unittest
from openapi3_discoverer import OpenApi3ApiDiscover
import os, sys
from pathlib import Path

parentDir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentDir)
from eventstore import EventStore

projectDirPath = os.path.dirname(Path(__file__))
sys.path.insert(0, projectDirPath)

class TestOpenApi3ApiDiscover(unittest.TestCase):
    
    def test_openapi3_get_params_path_object_yaml(self):
        
        apiFilePath = os.path.join(projectDirPath, 'testdata\\testdata-openapi3-get-params-path-object.yaml') 
    
        openapi3 = OpenApi3ApiDiscover(EventStore())
        
        apicontext = openapi3.load_openapi3_file(apiFilePath)
        
        self.assertTrue(apicontext is not None)
        
        self.assertTrue(len(apicontext.apis) == 1)
        
        api = apicontext.apis[0]
        
        self.assertTrue(len(api.parameters) == 4)
        
        paramProp1 = api.parameters[1]
        paramProp2 = api.parameters[2]
        paramProp3 = api.parameters[3]
        
        self.assertEqual(paramProp1.paramType, 'query')
        self.assertEqual(paramProp1.propertyName, 'complexObject')
        self.assertEqual(paramProp1.parameters[0].propertyName ,'foo')
        self.assertEqual(paramProp1.parameters[0].type , 'string')
        self.assertEqual(paramProp1.parameters[1].propertyName, 'color')
        self.assertEqual(paramProp1.parameters[1].type, 'string')
        
        self.assertEqual(paramProp2.paramType, 'query')
        self.assertEqual(paramProp2.propertyName, 'doubleParam')
        self.assertEqual(paramProp2.type , 'array')
        self.assertEqual(paramProp2.arrayProp.type, 'integer')
        
        self.assertEqual(paramProp3.paramType, 'query')
        self.assertEqual(paramProp3.propertyName, 'singleArray')
        self.assertEqual(paramProp3.type , 'array')
        self.assertEqual(paramProp3.arrayProp.type, 'string')
        
    
    # post_multipart-form-data
    def test_openapi3_post_multipart_form_data(self):
        
        apiFilePath = os.path.join(projectDirPath, 'testdata\\testdata-openapi3-post_multipart-form-data.yaml') 
    
        openapi3 = OpenApi3ApiDiscover(EventStore())
        
        apicontext = openapi3.load_openapi3_file(apiFilePath)
        
        self.assertTrue(apicontext is not None)
        
        self.assertTrue(len(apicontext.apis) == 1)
        
        api1 = apicontext.apis[0]
        
        apiParam1 = api1.body[0]
        apiParam2 = api1.body[1]
    
        self.assertEqual(api1.path, '/multipart-form-data/nestedjson-1')
        
        self.assertTrue(len(api1.body) == 2)
        
        self.assertEqual(apiParam1.propertyName, 'simple')
        self.assertEqual(apiParam1.type, 'string')
        
        self.assertEqual(apiParam2.propertyName, 'complex')
        self.assertEqual(apiParam2.type, 'array')
        self.assertEqual(apiParam2.arrayProp.type, 'object')
        
        # array containing complext object type
        arrayComplexObj = apiParam2.arrayProp.parameters
        
        self.assertTrue(len(arrayComplexObj) == 4)
        
        arrayComplexObjParam1 = arrayComplexObj[0]
        arrayComplexObjParam2 = arrayComplexObj[1]
        arrayComplexObjParam3 = arrayComplexObj[2]
        arrayComplexObjinnerObject = arrayComplexObj[3]
        
        self.assertEqual(arrayComplexObjParam1.propertyName, 'key')
        self.assertEqual(arrayComplexObjParam1.type, 'string')
        
        self.assertEqual(arrayComplexObjParam2.propertyName, 'size')
        self.assertEqual(arrayComplexObjParam2.type, 'integer')
        
        self.assertEqual(arrayComplexObjParam3.propertyName, 'nestyArrays1')
        self.assertEqual(arrayComplexObjParam3.type, 'array')
        self.assertEqual(arrayComplexObjParam3.arrayProp.type, 'string')
        
        self.assertEqual(arrayComplexObjinnerObject.propertyName, 'innerObject')
        self.assertEqual(arrayComplexObjinnerObject.type, 'object')
        
        innerNestedComplexObjectId = arrayComplexObjinnerObject.parameters[0]
        innerNestedComplexObjectAddress= arrayComplexObjinnerObject.parameters[1]
        innerNestedComplexObjectProfileImage = arrayComplexObjinnerObject.parameters[2]
        
        self.assertEqual(innerNestedComplexObjectId.propertyName, 'id')
        self.assertEqual(innerNestedComplexObjectId.type, 'string')
        self.assertEqual(innerNestedComplexObjectId.format, 'uuid')
        
        self.assertEqual(innerNestedComplexObjectAddress.propertyName, 'address')
        self.assertEqual(innerNestedComplexObjectAddress.type, 'object')
        self.assertEqual(innerNestedComplexObjectAddress.parameters[0].propertyName, 'street')
        self.assertEqual(innerNestedComplexObjectAddress.parameters[0].type, 'string')
        self.assertEqual(innerNestedComplexObjectAddress.parameters[1].propertyName, 'city')
        self.assertEqual(innerNestedComplexObjectAddress.parameters[1].type, 'string')
        
        self.assertEqual(innerNestedComplexObjectProfileImage.propertyName, 'profileImage')
        self.assertEqual(innerNestedComplexObjectProfileImage.type, 'string')
        self.assertEqual(innerNestedComplexObjectProfileImage.format, 'binary')
        
    
    # post_multipart-form-data
    def test_openapi3_post_requestbody_with_parameters(self):
        
        apiFilePath = os.path.join(projectDirPath, 'testdata\\testdata-openapi3-post-requestbody-with-parameters.yaml') 
    
        openapi3 = OpenApi3ApiDiscover(EventStore())
        
        apicontext = openapi3.load_openapi3_file(apiFilePath)
        
        self.assertTrue(True == True)

        
        
        
        

        
        
        
        
    
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