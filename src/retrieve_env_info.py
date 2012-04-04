#!/usr/bin/env python
import roslib 
roslib.load_manifest('task_planner')
roslib.load_manifest('knowledge_server')

from task_planner.srv import *
from task_planner.msg import *
from knowledge_server.srv import *
import rospy
import json

def handle_get_workspace(req):
    print '%s' % req.map
    query = exec_query("");

def get_workspace_service():
    rospy.init_node('retrieve_env_info_server')
    s = rospy.Service('get_workspace_on_map', GetWorkspaceOnMap, handle_get_workspace)
    print 'Ready -- get_workspace_service'
    rospy.spin()

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

if __name__ == "__main__":
    get_workspace_service()
