#!/usr/bin/env python3

import rospy
import socket
from tcp_repeater.msg import Bytes
from time import sleep

class TcpRepeater():
    def __init__(self):
        rospy.init_node("tcp_repeater")
        self.host = rospy.get_param("~host", "localhost")
        self.port = rospy.get_param("~port", 9001)
        self.bufsize = rospy.get_param("~bufsize", 4096)
        self.s = None
        self.connected = False
        self.data_pub = rospy.Publisher("tcp_data_out", Bytes, queue_size=1)

    def start(self):
        # Create a TCP/IP socket
        while not rospy.is_shutdown() and not self.connected:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.host, self.port))
                self.connected = True
            except socket.error:
                print("Connection failed. Retrying")
                sleep(1)
        print("Successfully connected to %s:%d" % (self.host, self.port))

    def run(self):
        while not rospy.is_shutdown():
            data = self.s.recv(self.bufsize)
            print('received "%s"\n' % data)
            print("Message length: %d\n" % len(data))
            byte_array = Bytes()
            byte_array.header.stamp = rospy.Time.now()
            byte_array.data = data
            self.data_pub.publish(byte_array)

    def stop(self):
        print("Closing socket")
        self.s.close()

if __name__ == "__main__":
    try:
        tcp_repeater = TcpRepeater()
        tcp_repeater.start()
        tcp_repeater.run()
    except KeyboardInterrupt:
        tcp_repeater.stop()
    finally:
        tcp_repeater.stop()

