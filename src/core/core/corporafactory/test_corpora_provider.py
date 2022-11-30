

import unittest
from corpora_provider import CorporaProvider

class TestImageCorpora(unittest.TestCase):
    
    def test_image_corpora(self):
        
        g = CorporaProvider()
        ok, err = g.load_all()
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        fval = g.fileCorpora.next_corpora()
        self.assertTrue(fval != None)
        
        boolval = g.boolCorpora.next_corpora()
        self.assertTrue(boolval != '')
        
        charval = g.charCorpora.next_corpora()
        self.assertTrue(charval != '')
        
        dtval = g.datetimeCorpora.next_corpora()
        self.assertTrue(dtval !=  None)
        
        dval = g.datetimeCorpora.next_date_corpora()
        self.assertTrue(dval !=  None)
        
        tval = g.datetimeCorpora.next_time_corpora()
        self.assertTrue(tval !=  None)
        
        dgval = g.digitCorpora.next_corpora()
        self.assertTrue(dgval !=  None)
        
        fval = g.fileCorpora.next_corpora()
        self.assertTrue(fval !=  None)
        
        imgval = g.imageCorpora.next_corpora()
        self.assertTrue(imgval !=  None)
        
        pdfval = g.pdfCorpora.next_corpora()
        self.assertTrue(pdfval !=  None)
        
        seclval = g.seclistPayloadCorpora.next_corpora()
        self.assertTrue(seclval !=  None)
        
        strval = g.stringCorpora.next_corpora()
        self.assertTrue(strval !=  None)
        
        xssval = g.stringCorpora.next_xss_corpora()
        self.assertTrue(xssval !=  None)
        
        sqlival = g.stringCorpora.next_sqli_corpora()
        self.assertTrue(sqlival !=  None)
        
        blnsval = g.stringCorpora.next_blns_corpora()
        self.assertTrue(blnsval !=  None)
        
        uval = g.usernameCorpora.next_corpora()
        self.assertTrue(uval !=  None)
        
        pval = g.passwordCorpora.next_corpora()
        self.assertTrue(pval !=  None)
        
        
if __name__ == '__main__':
    unittest.main()