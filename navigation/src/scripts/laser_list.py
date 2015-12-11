#!/usr/bin/env python
__author__ = 'andrii.kudriashov@gmail.com'

import rospy
import math
import laser_geometry
import json
from numpy import arange, around
from sensor_msgs.msg import LaserScan
from time import sleep, strftime
import zmq
import sensor_msgs.point_cloud2 as pc2

# zmq_publisher settings
zmq_port = "50601"
zmq_context = zmq.Context()
print "Publishing..."
zmq_socket = zmq_context.socket(zmq.PUB)
zmq_socket.bind("tcp://*:%s" % zmq_port)
geometry = laser_geometry.LaserProjection()


def generate_map(scan):
    mapa_pc2 = []
    cloud = geometry.projectLaser(scan_in=scan)
    gen = pc2.read_points(cloud, skip_nans=True, field_names=("x", "y", "z"))
    for point in gen:
        x, y, z = point
        # TODO: fix x,y
        mapa_pc2.append([y, x])

    return mapa_pc2


def callback(scan):
    # rospy.loginfo("some message")
    mapa = generate_map(scan)
#    sleep(1)
    for elem in mapa:
        elem[:] = [format(x, '.5f') for x in elem]
    del mapa[::2]
    del mapa[::2]
    del mapa[::2]

    mapa_string = json.dumps(mapa)
    #print "%s, %s" % ("mapa:", mapa_string)
    zmq_socket.send("%s, %s" % ("mapa:", mapa_string))

    #print mapa_string



def listener():
    rospy.init_node('listener_karmeluk')
    rospy.Subscriber("most_intense", LaserScan, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
