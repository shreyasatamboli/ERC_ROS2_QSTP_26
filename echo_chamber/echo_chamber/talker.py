#!/usr/bin/env python3
import rclpy
import random
from rclpy.node import Node
from std_msgs.msg import Float32

class RandomNumberGenerator(Node):

    def __init__(self):
        super().__init__("random_number")
        self.generate_rand_=self.create_publisher(Float32,"/random_number",10)
        self.timer_= self.create_timer(1,self.randGenerator)
        self.get_logger().info("Random Number Generator has started")

    def randGenerator (self):
        msg = Float32()
        msg.data=random.uniform(1,100)
        self.generate_rand_.publish(msg)



def main(args=None):
    rclpy.init(args=args)
    node=RandomNumberGenerator()
    rclpy.spin(node)
    rclpy.shutdown()