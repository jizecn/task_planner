#!/usr/bin/env python
#################################################################
##\file
#
# \note
# Copyright (c) 2012 \n
# Cardiff University \n\n
#
#################################################################
#
# \note
# Project name: Multi-Role Shadow Robotic System for Independent Living
# \note
# ROS stack name: srs
# \note
# ROS package name: retrieve_env_info_server
#
# \author
# Author: Ze Ji, email: jizecn (at) gmail.com
#
# \date Date of creation: Feb 2012
#
# \brief
# Services to query semantic DB and parse results into ROS services 
#
#################################################################
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer. \n
#
# - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution. \n
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License LGPL as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License LGPL for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License LGPL along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
#################################################################
import roslib 
roslib.load_manifest('task_planner')
roslib.load_manifest('knowledge_server')

from task_planner.srv import *
from task_planner.msg import *
from knowledge_server.srv import *
import rospy
import json
from jsonparser import JSONResultParser
from geometry_msgs.msg import *
from knowledge_interface import exec_query

def handle_get_workspace(req):
    print '%s' % req.map
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT DISTINCT ?objs ?hhid ?x ?y ?z ?qx ?qy ?qz ?qw ?w ?h ?l
        WHERE { ?objs a srs:FurniturePiece .
        ?objs srs:houseHoldObjectID ?hhid .
        OPTIONAL {
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
        }
        }
        """)
    print res

    result = GetWorkspaceOnMapResponse()
    res_json_parser = JSONResultParser(res)

    result.objects = res_json_parser.get_result_by_varname('objs')

    hhids_int = res_json_parser.get_result_by_varname('hhid')
    result.houseHoldId = list()
    
    for hhid_int in hhids_int:
        result.houseHoldId.append(str(hhid_int))

    spainfo = res_json_parser.get_spaital_info()
    result.objectsInfo = spainfo
    return result

def get_workspace_service():
    #rospy.init_node('retrieve_env_info_server')
    s = rospy.Service('get_workspace_on_map', GetWorkspaceOnMap, handle_get_workspace)
    print 'Ready -- get_workspace_service'
    #rospy.spin()

def handle_get_objects(req):
    print '%s' % req.map
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT DISTINCT ?objs ?hhid ?x ?y ?z ?qx ?qy ?qz ?qw ?w ?h ?l
        WHERE { ?objs a srs:FoodVessel .
        ?objs srs:houseHoldObjectID ?hhid .
        OPTIONAL {
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
        }
        }
        """)
    print res

    result = GetObjectsOnMapResponse()
    res_json_parser = JSONResultParser(res)

    result.objects = res_json_parser.get_result_by_varname('objs')

    hhids_int = res_json_parser.get_result_by_varname('hhid')
    result.houseHoldId = list()
    
    for hhid_int in hhids_int:
        result.houseHoldId.append(str(hhid_int))

    spainfo = res_json_parser.get_spaital_info()
    result.objectsInfo = spainfo
    return result

def get_objects_service():
    #rospy.init_node('retrieve_objects_info_server')
    s = rospy.Service('get_objects_on_map', GetObjectsOnMap, handle_get_objects)
    print 'Ready -- get_objects_service'
    #rospy.spin()

def handle_get_rooms(req):
    print '%s' % req.map
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ipa-kitchen: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT ?objs
        WHERE { ?objs rdf:type srs:RoomInAConstruction .
        OPTIONAL {
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
        }
        }
        """);
    
    print res
    
    result = GetRoomsOnMapResponse()
    res_json_parser = JSONResultParser(res)
    result.rooms = res_json_parser.get_result_by_varname('objs')
    spainfo = res_json_parser.get_spaital_info()
    result.roomsInfo = spainfo
    return result

def get_rooms_service():
    s = rospy.Service('get_rooms_on_map', GetRoomsOnMap, handle_get_rooms)
    print 'Ready -- get_rooms_service'

def handle_get_predefined_poses(req):
    print 'get_predefined_poses -- %s' % req.map
    res = exec_query(
        """
        PREFIX srs: <http://www.srs-project.eu/ontologies/srs.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX map-name: <http://www.srs-project.eu/ontologies/ipa-kitchen.owl#>
        SELECT ?poses ?x ?y ?theta
        WHERE {
        ?poses rdf:type srs:Point2D .
        ?poses srs:xCoordinate ?x .
        ?poses srs:yCoordinate ?y .
        ?poses srs:orientationTheta ?theta .
        }
        """);
    
    print res
    
    result = GetPredefinedPosesResponse()
    res_json_parser = JSONResultParser(res)
    result = res_json_parser.get_predefined_poses()
   
    return result

def get_predefined_poses_service():
    s = rospy.Service('get_predefined_poses', GetPredefinedPoses, handle_get_predefined_poses)
    print 'Ready -- get_predefined_poses_service'

if __name__ == "__main__":
    rospy.init_node('retrieve_env_info_server')
    get_workspace_service()
    get_objects_service()
    get_rooms_service()
    get_predefined_poses_service()
    rospy.spin()
