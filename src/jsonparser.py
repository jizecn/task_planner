#!/usr/bin/env python
import roslib 
roslib.load_manifest('task_planner')
roslib.load_manifest('knowledge_server')

from task_planner.srv import *
from task_planner.msg import *

import json
from StringIO import StringIO
import rdflib

class JSONResultParser:
    def __init__(self, json_raw_string):
        self.json_raw_string = json_raw_string
        self.json_decoded = json.loads(self.json_raw_string)
        
    def get_result_by_varname(self, varname):
        print 'RUN- GET_RESULT_BY_VARNAME'
        #print self.json_raw_string
        ress = self.json_decoded['results']['bindings']
        # now [ress] is a list
        l = len(ress)
        ret = list()
        
        for r in ress:
            if r[varname]['type'] == 'uri':
                s = str(r[varname]['value'])
                #print 'value of URI: ', s
                localname_s = s.rsplit('#', 1)[1]
                ret.append(localname_s)
            elif r[varname]['type'] == 'typed-literal':
                if r[varname]['datatype'] == 'http://www.w3.org/2001/XMLSchema#int':
                    s = int(r[varname]['value'])
                    #print 'value of int: ', s
                    ret.append(s)

        return ret
        
    def get_spaital_info(self):
        print 'RUN- GET_SPATIAL_INFO'
        ress = self.json_decoded['results']['bindings']
        # now [ress] is a list
        l = len(ress)
        print 'Size is %d', l
        ret = list()
        
        for r in ress:
            spainfo = SRSSpatialInfo()
            spainfo.w = -1000
            spainfo.h = -1000
            spainfo.l = -1000
            spainfo.pose.position.x = -1000
            spainfo.pose.position.y = -1000
            spainfo.pose.position.z = -1000
            spainfo.pose.orientation.x = -1000
            spainfo.pose.orientation.y = -1000
            spainfo.pose.orientation.z = -1000
            spainfo.pose.orientation.w = -1000
            if r['l']['type'] == 'typed-literal':
                if r['l']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.l = float(r['l']['value'])
            if r['h']['type'] == 'typed-literal':
                if r['h']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.h = float(r['h']['value'])
            if r['w']['type'] == 'typed-literal':
                if r['w']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.w = float(r['w']['value'])
            if r['x']['type'] == 'typed-literal':
                if r['x']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.position.x = float(r['w']['value'])
            if r['y']['type'] == 'typed-literal':
                if r['y']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.position.y = float(r['y']['value'])
            if r['z']['type'] == 'typed-literal':
                if r['z']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.position.z = float(r['z']['value'])
            if r['qx']['type'] == 'typed-literal':
                if r['qx']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.x = float(r['qx']['value'])
            if r['qy']['type'] == 'typed-literal':
                if r['qy']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.y = float(r['qy']['value'])
            if r['qz']['type'] == 'typed-literal':
                if r['qz']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.z = float(r['qz']['value'])
            if r['qw']['type'] == 'typed-literal':
                if r['qw']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.w = float(r['qw']['value'])

            ret.append(spainfo)
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

