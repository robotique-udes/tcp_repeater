#!/usr/bin/env python3

import rospy
import socket
from tcp_repeater.msg import Bytes
from time import sleep

class TcpPublisher:
    def __init__(self):
        rospy.init_node("tcp_publisher")
        self.host = rospy.get_param("~host", "localhost")
        self.port = rospy.get_param("~port", 9001)
        self.bufsize = rospy.get_param("~bufsize", 4096)
        self.connected = False
        self.s = None
        rospy.Subscriber("tcp_data_out", Bytes, callback=self.data_cb)

    def start(self):
        # Create a TCP/IP socket
        print("Attempting to connect to %s:%d" % (self.host, self.port))
        while not rospy.is_shutdown() and not self.connected:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.host, self.port))
                self.connected = True
            except socket.error:
                print("Connection failed. Retrying")
                sleep(1)
        print("Successfully connected to %s:%d" % (self.host, self.port))

    def stop(self):
        print("Closing socket")
        self.s.close()

    def data_cb(self, msg):
        if self.s != None and not self.connected:
            print("sending")
            self.conn.sendall(msg.data)


if __name__ == "__main__":
    try:
        tcp_pub = TcpPublisher()
        tcp_pub.start()
        rospy.spin()
    except KeyboardInterrupt:
        tcp_pub.stop()
    finally:
        tcp_pub.stop()
