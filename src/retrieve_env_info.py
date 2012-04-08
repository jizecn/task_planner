#!/usr/bin/env python
import roslib 
roslib.load_manifest('task_planner')
roslib.load_manifest('knowledge_server')

from task_planner.srv import *
from task_planner.msg import *
from knowledge_server.srv import *
import rospy
import json
from jsonparser import JSONResultParser

def handle_get_workspace(req):
    print '%s' % req.map
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT ?objs ?x ?y ?z ?w ?h ?l
        WHERE { ?objs rdf:type srs:FurniturePiece .
        ?objs srs:xCoord ?x .
        ?objs srs:yCoord ?y .
        ?objs srs:zCoord ?z .
        ?objs srs:widthOfObject ?w .
        ?objs srs:heightOfObject ?h .
        ?objs srs:lengthOfObject ?l . }
        """);
    
    #print res
    
    result = GetWorkspaceOnMapResponse()
    res_json_parser = JSONResultParser(res)
    result.objects = res_json_parser.get_result_by_varname('objs')
    return result

def __get_result_by_var(res, varname):
    try:
        decres = json.loads(res)
        
    except:
        print "Unexpected error:", sys.exc_info()[0]
    
    return None

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
