#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_srvs.srv import SetBool

class Avoid(Node):

    def __init__(self):
        super().__init__("avoider")
        self.is_active = False 
        self.cmd_vel_pub_= self.create_publisher(Twist,"/cmd_vel",10)
        self.laser_scan_=self.create_subscription(LaserScan, "/scan", self.scan_callback,  10)
        self.srv = self.create_service(SetBool, '/toggle_robot', self.toggle_callback)
        self.get_logger().info("Avoider has started")

        self.obstacle_dist = 1.0
        self.spiral_lin = 0.001 
        self.spiral_ang = 1

        self.state = "SPIRAL"

    def toggle_callback(self, request, response):
        self.is_active = request.data
        if self.is_active:
            self.state= "SPIRAL"
        response.success = True
        response.message = f"Robot is now {'ON' if self.is_active else 'OFF'}"
        return response

    def clean(self, values):
        return [v if (math.isfinite(v)) else 10.0 for v in values]

    def now_sec(self):
        return self.get_clock().now().nanoseconds * 1e-9

    def scan_callback(self, msg):
        cmd=Twist()

        if not self.is_active:
            self.cmd_vel_pub_.publish(cmd)
            return

        r = msg.ranges
        front = self.clean(list(r[:45]) + list(r[-45:]))
        front_min = min(front)
        left = self.clean([r[90]])[0]
        right = self.clean([r[270]])[0]

        if front_min<self.obstacle_dist:
            self.state = "AVOID"

        else:
            self.state = "SPIRAL"

        if self.state == "SPIRAL":
            cmd.linear.x = self.spiral_lin
            self.spiral_lin += 0.002
            cmd.angular.z = self.spiral_ang

        elif self.state == "AVOID":
            cmd.linear.x = 0.0
            cmd.linear.z = 0.0
            cmd.linear.y = 0.0
            if right>left:
                cmd.angular.z = -1.0

            elif left>right :
                cmd.angular.z = 1.0

            else:
                cmd.angular.z = -1.0

        self.cmd_vel_pub_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node=Avoid()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()