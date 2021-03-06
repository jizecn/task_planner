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
# ROS package name: planner
#
# \author
# Author: Ze Ji, email: jizecn (at) gmail.com
#
# \date Date of creation: March 2012
#
# \brief
# High level task planner
# (Re-write srs_knowledge in Python)
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
import action_knowledge_engine as eng

def handle_task_request(req):
    result = TaskRequestResponse()
    rospy.loginfo(req.task + '  ' + req.content)

    # look for final state based on task type
    wstates = eng.get_world_states()
    print wstates
    
    # calculate solutions
    
    return result

def task_request_service():
    s = rospy.Service('task_request', TaskRequest, handle_task_request)
    print 'Ready -- get_objects_service'

def usage():
    print """
    To run this package:  rosrun task_planner planner.py
    """

if __name__ == "__main__":
    """
    task planner
    -- re-write the legacy code in a more generic way
    -- and separate the work into different functional packages for easier maintenance
    """
    usage()
    print 'start now... '
    
    rospy.init_node('task_planner_node')
    task_request_service()
    rospy.spin()
