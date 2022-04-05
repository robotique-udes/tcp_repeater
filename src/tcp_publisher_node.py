#!/usr/bin/env python3

import rospy
import socket
from tcp_repeater.msg import Bytes

class TcpPublisher:
    def __init__(self):
        rospy.init_node("tcp_publisher")
        self.host = rospy.get_param("~host", "localhost")
        self.port = rospy.get_param("~port", 9001)
        self.bufsize = rospy.get_param("~bufsize", 4096)
        self.conn = None
        self.s = None
        rospy.Subscriber("tcp_data_in", Bytes, callback=self.data_cb)

    def start(self):
        # Create a TCP/IP socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connect the socket to the port where the server is listening
        print('Starting server on %s:%s' % (self.host, self.port))
        self.s.bind((self.host, self.port))
        self.s.listen()
        self.conn, addr = self.s.accept()
        print("Connection established with " + str(addr))

    def stop(self):
        print("Closing socket")
        self.s.close()

    def data_cb(self, msg):
        print("data received")
        if self.s != None and self.conn != None:
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
