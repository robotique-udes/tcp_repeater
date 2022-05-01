# tcp_repeater
The purpose of this package is to publish TCP messages into the ROS network to easily distribute them across multiple machines and to then republish them out of the ROS network elsewhere, without having to mess with IP configurations. It is espacially useful if you are working with devices that lack the ability to change network settings. This package was made to make it easier to use the Emlid Reach RTK GPS with ROS.<br><br>
Both the repeater and publisher node are setup as clients, so the sockets they are connecting to must be setup as servers.

# tcp_repeater_node
Connects to a TCP socket server and publishes the received messages as ROS messages.
## Published topics
* tcp_data_out (tcp_repeater/Bytes): Received data as a byte array

## Parameters
* ~host (string, default: "localhost"): Host name or IP address of the server the node will connect to.
* ~port (int, default: 9001): Port number of the server the node will connect to.
* ~bufsize (int, default: 4096): Buffer size for the message reception.

# tcp_publisher_node
Subscribes to the ROS topic containing the data and publishes it to a TCP socket server.
## Subscribed topics
* tcp_data_out (tcp_repeater/Bytes): Received data as a byte array
## Parameters
* ~host (string, default: "localhost"): Host name or IP address of the server the node will connect to.
* ~port (int, default: 9001): Port number of the server the node will connect to.
* ~bufsize (int, default: 4096): Buffer size for the message reception.

# Setup
1. To make python3 compatible with ROS Melodic:
    ```
    sudo apt-get install python3-catkin-pkg-modules
    sudo apt-get install python3-rospkg-modules
    ```