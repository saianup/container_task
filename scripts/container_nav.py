import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np


class ContainerNav(Node):

    def __init__(self):
        super().__init__('container_nav')

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.entered = False
        self.reversing = False

        self.WALL_DETECT = 2.5
        self.BACK_WALL = 0.7


    def scan_callback(self, msg):

        ranges = np.array(msg.ranges)
        ranges[np.isinf(ranges)] = 10.0

        n = len(ranges)

        left = np.mean(ranges[int(0.70*n):int(0.80*n)])
        right = np.mean(ranges[int(0.20*n):int(0.30*n)])
        front = np.mean(ranges[int(0.48*n):int(0.52*n)])

        cmd = Twist()

        if not self.entered:

            cmd.linear.x = 0.20

            if left < self.WALL_DETECT and right < self.WALL_DETECT:
                self.entered = True
                self.get_logger().info("Entered container")


        elif not self.reversing:

            error = left - right

            if abs(error) < 0.05:
                turn = 0.0
            else:
                turn = -0.3 * error

            turn = np.clip(turn, -0.25, 0.25)

            cmd.linear.x = 0.25
            cmd.angular.z = turn

            if front < self.BACK_WALL:
                self.reversing = True
                self.get_logger().info("Reached back wall")


        else:

            error = left - right

            if abs(error) < 0.05:
                turn = 0.0
            else:
                turn = -0.3 * error

            turn = np.clip(turn, -0.25, 0.25)

            cmd.linear.x = -0.25
            cmd.angular.z = turn

            if front > 7.0:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.get_logger().info("Exited container")


        self.cmd_pub.publish(cmd)


def main(args=None):

    rclpy.init(args=args)

    node = ContainerNav()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()