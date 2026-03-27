import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Importaciones de la SDK de Unitree
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

class B2BridgeNode(Node):
    def __init__(self):
        super().__init__('b2_bridge_node')
        
        # 1. Inicializar comunicación de Unitree. 
        # "lo" es para Isaac Sim local. Si es el robot real, usa su interfaz (ej. "eth0")
        self.interface = "lo"
        ChannelFactoryInitialize(0, self.interface)
        
        # 2. Crear el cliente de movimiento (SportClient)
        self.sport_client = SportClient()
        self.sport_client.Init()
        
        # 3. Crear suscriptor a /cmd_vel (el estándar de ROS)
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        
        self.get_logger().info(f'Nodo B2 Bridge iniciado en interfaz: {self.interface}')

    def listener_callback(self, msg):
        # Extraer velocidades del mensaje ROS
        x = msg.linear.x
        y = msg.linear.y
        yaw = msg.angular.z
        
        # 4. Enviar a la SDK de Unitree
        # Move(x_speed, y_speed, yaw_speed)
        self.sport_client.Move(x, y, yaw)
        
        self.get_logger().info(f'Enviando a B2 -> x: {x}, y: {y}, yaw: {yaw}')

def main(args=None):
    rclpy.init(args=args)
    node = B2BridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Deteniendo nodo...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()