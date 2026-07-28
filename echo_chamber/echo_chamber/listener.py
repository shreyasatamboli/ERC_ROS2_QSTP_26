#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class RandCatcher(Node):

    def __init__(self):
        super().__init__("listener")
        self.pose_subscriber_ = self.create_subscription(Float32, "/random_number",self.rand_callback,10)

    def rand_callback(self, msg: Float32):
        x = (msg.data)*2
        self.get_logger().info("Recieved: " + str(msg.data) + " Multiplied value: " + str(x))

def main(args=None):
    rclpy.init(args=args)
    node=RandCatcher()
    rclpy.spin(node)
    rclpy.shutdown()