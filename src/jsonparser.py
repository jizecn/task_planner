#!/usr/bin/env python
import roslib 
roslib.load_manifest('task_planner')
roslib.load_manifest('knowledge_server')

from task_planner.srv import *
from task_planner.msg import *
from geometry_msgs.msg import *
import json
from StringIO import StringIO
#import rdflib

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

    def get_predefined_poses(self):
        print 'RUN - GET PREDEFINED POSES AS TUPLE'
        #print self.json_raw_string
        ress = self.json_decoded['results']['bindings']
        # now [ress] is a list
        l = len(ress)

        result = GetPredefinedPosesResponse()
        
        locs = list()
        poses = list()

        for r in ress:
            varname = 'poses'
            if r[varname]['type'] == 'uri':
                s = str(r[varname]['value'])
                #print 'value of URI: ', s
                localname_s = s.rsplit('#', 1)[1]
            else:
                pass
            tempPose = Pose2D()

            varname = 'x'
            if r[varname]['type'] == 'typed-literal':
                if r[varname]['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    s = float(r[varname]['value'])
                    #print 'value of int: ', s
                    tempPose.x = s
                    #tempPose.append(s)
                else:
                    pass
            else:
                pass

            varname = 'y'
            if r[varname]['type'] == 'typed-literal':
                if r[varname]['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    s = float(r[varname]['value'])
                    #print 'value of int: ', s
                    tempPose.y = s
                    #tempPose.append(s)
                else:
                    pass
            else:
                pass

            varname = 'theta'
            if r[varname]['type'] == 'typed-literal':
                if r[varname]['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    s = float(r[varname]['value'])
                    #print 'value of int: ', s
                    tempPose.theta = s
                    #tempPose.append(s)
                else:
                    pass
            else:
                pass

            locs.append(localname_s)
            poses.append(tempPose)

        result.locations = locs
        result.poses = poses
        return result
        
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
            if r.has_key('l') and r['l']['type'] == 'typed-literal':
                if r['l']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.l = float(r['l']['value'])
            if r.has_key('h') and r['h']['type'] == 'typed-literal':
                if r['h']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.h = float(r['h']['value'])
            if r.has_key('w') and r['w']['type'] == 'typed-literal':
                if r['w']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.w = float(r['w']['value'])
            if r.has_key('x') and r['x']['type'] == 'typed-literal':
                if r['x']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.position.x = float(r['x']['value'])
            if r.has_key('y') and r['y']['type'] == 'typed-literal':
                if r['y']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.position.y = float(r['y']['value'])
            if r.has_key('z') and r['z']['type'] == 'typed-literal':
                if r['z']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.position.z = float(r['z']['value'])
            if r.has_key('qx') and r['qx']['type'] == 'typed-literal':
                if r['qx']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.x = float(r['qx']['value'])
            if r.has_key('qy') and r['qy']['type'] == 'typed-literal':
                if r['qy']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.y = float(r['qy']['value'])
            if r.has_key('qz') and r['qz']['type'] == 'typed-literal':
                if r['qz']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.z = float(r['qz']['value'])
            if r.has_key('qw') and r['qw']['type'] == 'typed-literal':
                if r['qw']['datatype'] == 'http://www.w3.org/2001/XMLSchema#float':
                    spainfo.pose.orientation.w = float(r['qw']['value'])

            ret.append(spainfo)
        return ret

    #@staticmethod
    def get_single_spaital_info(self, query_res):
        print 'RUN- GET_SPATIAL_INFO'

        res_dec = json.loads(query_res)
        ress = res_dec['results']['bindings']
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

        if len(ress) == 1:
            r = ress[0]
        else:
            return spainfo
        
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

        return spainfo 

    def parse_into_world_states(self):
        return None
    
def test():
    json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    print json.dumps("\"foo\bar")
    print json.dumps(u'\u1234')
    print json.dumps('\\')
    print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
    io = StringIO()
    json.dump(['streaming API'], io)
    io.getvalue()

