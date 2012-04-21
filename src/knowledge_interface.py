#!/usr/bin/env python
import roslib 
roslib.load_manifest('task_planner')
roslib.load_manifest('knowledge_server')
from task_planner.srv import *
from task_planner.msg import *
from knowledge_server.srv import *
from geometry_msgs.msg import *

import rospy

def exec_query(query):
    print 'exec sparql query'
    rospy.wait_for_service('query_sparql')
    try:
        query_sparql_service = rospy.ServiceProxy('query_sparql', QuerySparQL)
        req = QuerySparQLRequest()
        req.query = query
        res = query_sparql_service(req);
        return res.result
    except rospy.ServiceException, e:
        print "Service call (QuerySparQL) failed : %s"%e

def exec_terp_query(query):
    print 'exec terp query'
    rospy.wait_for_service('query_terp')
    try:
        query_terp_service = rospy.ServiceProxy('query_terp', QueryTerp)
        req = QueryTerpRequest()
        req.query = query
        res = query_terp_service(req);
        return res.result
    except rospy.ServiceException, e:
        print "Service call (QueryTerp) failed : %s"%e
