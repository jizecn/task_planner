#!/usr/bin/env python
import roslib 
roslib.load_manifest('task_planner')
roslib.load_manifest('knowledge_server')

import rospy
from task_planner.srv import *
from task_planner.msg import *
from knowledge_server.srv import *
from jsonparser import JSONResultParser

def handle_get_rooms(req):
    print '%s' % req.map
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT ?objs ?x ?y ?z ?w ?h ?l ?qx ?qy ?qz ?qw ?hhid
        WHERE { ?objs rdf:type srs:FurniturePiece .
        ?objs srs:xCoord ?x .
        ?objs srs:yCoord ?y .
        ?objs srs:zCoord ?z .
        ?objs srs:qx ?qx .
        ?objs srs:qy ?qy .
        ?objs srs:qz ?qz .
        ?objs srs:qu ?qw .
        ?objs srs:widthOfObject ?w .
        ?objs srs:heightOfObject ?h .
        ?objs srs:lengthOfObject ?l .
        ?objs srs:houseHoldObjectID ?hhid . }
        """);
    
    #print res
    
    result = GetWorkspaceOnMapResponse()
    res_json_parser = JSONResultParser(res)
    result.objects = res_json_parser.get_result_by_varname('objs')
    spainfoList = res_json_parser.get_spaital_info()
    
    result.objectsInfo = spainfoList

    hhids_int = res_json_parser.get_result_by_varname('hhid')
    result.houseHoldId = list()
    
    for hhid_int in hhids_int:
        result.houseHoldId.append(str(hhid_int))
        
    return result

def get_rooms_service():
    rospy.init_node('retrieve_rooms_info_server')
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
