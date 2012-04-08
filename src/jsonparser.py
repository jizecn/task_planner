#!/usr/bin/env python
import json
from StringIO import StringIO


class JSONResultParser:
    def __init__(self, json_raw_string):
        self.json_raw_string = json_raw_string
        self.json_decoded = json.loads(self.json_raw_string)
        
    def get_result_by_varname(self, varname):
        print 'RUN- GET_RESULT_BY_VARNAME'
        ress = self.json_decoded['results']['bindings']
        # now [ress] is a list
        l = len(ress)
        print 'Size is %d', l
        ret = list()
        for r in ress:
            #print r
            if r[varname]['type'] == '':
                ret.append(str(r[varname]['value']))
            elif r[varname]['type'] == '.....float':
                ret.append(float(r[varname]['value]']))
            
        type(ret)
        print 'RUN- GET_RESULT_BY_VARNAME'
        print ret
        return ret
        
        
def test():
    json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    print json.dumps("\"foo\bar")
    print json.dumps(u'\u1234')
    print json.dumps('\\')
    print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
    io = StringIO()
    json.dump(['streaming API'], io)
    io.getvalue()

def decodeSparQLResult(res):
    decres = json.loads(res)
    return decres

def get_result(jsonres):
    return None
