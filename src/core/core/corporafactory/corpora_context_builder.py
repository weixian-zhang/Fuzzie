import os, sys
from pathlib import Path
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
sys.path.insert(0, os.path.join(core_core_dir, 'models'))

from models.webapi_fuzzcontext import (ApiFuzzCaseSet,)
from corpora_context import CorporaContext

class CorporaContextBuilder:
    
    def __init__(self, corporaContext: CorporaContext) -> None:
        self.cp = corporaContext
    
    def build_for_api(self, fcss: list[ApiFuzzCaseSet], tryBuild=False) -> tuple([bool, str]):
        
        try:
            self.cp.tryBuild = tryBuild
        
            for fcs in fcss:
                
                if not self.isWordlistTemplateEmpty(fcs.urlDataTemplate):
                    self.cp.build_data_context_from_req_msg(fcs.urlDataTemplate)
                
                # if not self.isWordlistTemplateEmpty(fcs.querystringDataTemplate):
                #     self.cp.build_data_context_from_req_msg(fcs.querystringDataTemplate)
                    
                if not self.isWordlistTemplateEmpty(fcs.headerDataTemplate):
                    self.cp.build_data_context_from_req_msg(fcs.headerDataTemplate)
                
                if not self.isWordlistTemplateEmpty(fcs.bodyDataTemplate):
                    self.cp.build_data_context_from_req_msg(fcs.bodyDataTemplate)
                    
                if not self.isWordlistTemplateEmpty(fcs.graphQLVariableDataTemplate):
                    self.cp.build_data_context_from_req_msg(fcs.graphQLVariableDataTemplate)
                    
                if not self.isWordlistTemplateEmpty(fcs.fileDataTemplate):
                    self.cp.build_data_context_from_req_msg(fcs.fileDataTemplate)
                    
            return True, ''
        
        except Exception as e:
            return False, ''
                 
                
    def isWordlistTemplateEmpty(self, template):
        if template == '' or template == '{}':
            return True
        return False