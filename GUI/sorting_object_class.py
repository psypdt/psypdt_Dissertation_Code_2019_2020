#! /usr/bin/env python

from __future__ import print_function

import rospy
from geometry_msgs.msg import PoseStamped
import json
import simplejson
from json import JSONEncoder
import StringIO


class SortableObject(object):
    static_object_counter = 1  # Static counter to track number of objects


    #  This method will generate JSON when the object needs to be serialised
    def __json__(self):
        return dict({
            'm_name': 20,
            'm_start_pose': {
                'header.seq': self.m_start_pose.header.seq,
                'header.stamp': self.m_start_pose.header.stamp,
                'header.frame_id': self.m_start_pose.header.frame_id,

                'position.x': self.m_start_pose.pose.position.x,
                'position.y': self.m_start_pose.pose.position.y,
                'position.z': self.m_start_pose.pose.position.z,

                'orientation.x': self.m_start_pose.pose.orientation.x,
                'orientation.y': self.m_start_pose.pose.orientation.y,
                'orientation.z': self.m_start_pose.pose.orientation.z,
                'orientation.w': self.m_start_pose.pose.orientation.w,
            },
            'm_end_pose': {
                'header.seq': self.m_end_pose.header.seq,
                'header.stamp': self.m_end_pose.header.stamp,
                'header.frame_id': self.m_end_pose.header.frame_id,

                'position.x': self.m_end_pose.pose.position.x,
                'position.y': self.m_end_pose.pose.position.y,
                'position.z': self.m_end_pose.pose.position.z,

                'orientation.x': self.m_end_pose.pose.orientation.x,
                'orientation.y': self.m_end_pose.pose.orientation.y,
                'orientation.z': self.m_end_pose.pose.orientation.z,
                'orientation.w': self.m_end_pose.pose.orientation.w,
            },
            '__python__': self.__module__+":SortableObject.from_json",
        })

    for_json = __json__  # To support simlejson

    #  cls is the class which is currently being used (don't need to pass it as arg when using this method)
    #  This method will convert from json back to an object
    @classmethod
    def from_json(cls, json):
        obj = cls()
        res_dict = eval(json)  # Create dictionary where values can be extracted from
        obj.m_name = res_dict["m_name"]
        obj.m_start_pose = res_dict['m_start_pose']
        obj.m_end_pose = res_dict['m_end_pose']
        
        return obj


    
    def __init__(self, obj_name="sortable", obj_start=None, obj_end=None):
        self.m_name = obj_name + str(SortableObject.static_object_counter)
        
        self.m_start_pose = obj_start  # Where object is initially located in the work space
        self.m_end_pose = obj_end  # The location of the container where the object should be placed

        SortableObject.static_object_counter += 1  # Increment number of objects

        print("Number of objects is: {}".format(SortableObject.static_object_counter))

        if self.m_start_pose == None:
            self.m_start_pose = PoseStamped()
        
        if self.m_end_pose == None:
            self.m_end_pose = PoseStamped()



if __name__ == '__main__':

    start = PoseStamped()
    start.header.seq = 1
    start.header.stamp = 1
    start.header.frame_id = 'map_lol_idk'

    #  Final Positions
    start.pose.position.x = 0.704020578925
    start.pose.position.y = 0.6890
    start.pose.position.z = 0.455

    #  Final Orientation
    start.pose.orientation.x = 0.0
    start.pose.orientation.y = 0.0
    start.pose.orientation.z = 0.0
    start.pose.orientation.w = 1.0
    

    final_pos = PoseStamped()

    final_pos.header.seq = 2
    final_pos.header.stamp = 0
    final_pos.header.frame_id = 'who knows'

    #  Final Positions
    final_pos.pose.position.x = 0.0
    final_pos.pose.position.y = 0.0
    final_pos.pose.position.z = 0.0

    #  Final Orientation
    final_pos.pose.orientation.x = 1.0
    final_pos.pose.orientation.y = 1.0
    final_pos.pose.orientation.z = 1.0
    final_pos.pose.orientation.w = 0.0

    obj = SortableObject(obj_name="idk", obj_start=start, obj_end=final_pos)

    # obj.m_start_pose = start
    # obj.m_end_pose = final_pos

    jsona = simplejson.dumps(obj, for_json=True)

    obj2_dict = simplejson.loads(jsona)
    obj2 = SortableObject.from_json(jsona)

    assert isinstance(obj2, SortableObject)

    print(obj2.m_end_pose)

    # help(PoseStamped)




