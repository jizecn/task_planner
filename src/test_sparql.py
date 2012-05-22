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

def handle_get_objects():
    #print '%s' % req.map
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT ?objs ?x ?y ?z ?w ?h ?l ?qx ?qy ?qz ?qw ?hhid
        WHERE { ?objs rdf:type srs:FoodVessel .
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
        ?objs srs:houseHoldObjectID ?hhid .}
        """)
    
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

def construct_sparql():
    #print '%s' % req.map
    res = exec_construct_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        CONSTRUCT
        {
        ?x srs:srsX ?objX .
        ?y srs:srsY ?objY .
        ?z srs:srsZ ?objZ .
        }
        WHERE
        {
        ?x srs:xCoord ?objX .
        ?y srs:yCoord ?objY .
        ?z srs:zCoord ?objZ .
        }
        """)
    
    return res

def exec_construct_query(query):
    print 'exec construct sparql query'
    rospy.wait_for_service('construct_rule')
    try:
        construct_sparql_service = rospy.ServiceProxy('construct_rule', ConstructRule)
        req = ConstructRuleRequest()
        req.constructRule = query
        res = construct_sparql_service(req);
        return res.result
    except rospy.ServiceException, e:
        print "Service call (QuerySparQL) failed : %s" %e

def handle_get_objects_new():
    #print '%s' % req.map
    
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT ?objs ?x ?y ?z ?w ?h ?l ?qx ?qy ?qz ?qw ?hhid
        WHERE { ?objs rdf:type srs:FoodVessel .
        ?objs srs:srsX ?x .
        ?objs srs:srsY ?y .
        ?objs srs:srsZ ?z .
        ?objs srs:qx ?qx .
        ?objs srs:qy ?qy .
        ?objs srs:qz ?qz .
        ?objs srs:qu ?qw .
        ?objs srs:widthOfObject ?w .
        ?objs srs:heightOfObject ?h .
        ?objs srs:lengthOfObject ?l .
        ?objs srs:houseHoldObjectID ?hhid .}
        """)

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

if __name__ == "__main__":
    #rospy.init_node('retrieve_objects_info_server')
    print handle_get_objects()
    print construct_sparql()
    print handle_get_objects_new()
    #get_objects_service()
    #rospy.spin()
