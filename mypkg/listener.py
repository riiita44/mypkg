import rclpy
from rclpy.node import Node
from person_msgs.srv import Query

rclpy.init()
node = Node("listener")


def main():
    client = node.create_client(Query, "query")

    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info("待機中")

    req = Query.Request()
    req.name = "岡野稜大"
    future = client.call_async(req)

    while rclpy.ok():
        rclpy.spin_once(node)   #通信の処理を1回だけ行う
        if future.done():       #返事が届いていたら
            try:
                response = future.result()   #返事を取り出す
            except:
                node.get_logger().info('呼び出し失敗')
            else:   #exceptにならなかったとき（成功したとき）
                node.get_logger().info("age: {}".format(response.age))   #年齢を表示

            break   #whileを出る

    node.destroy_node()   #ノードの後始末
    rclpy.shutdown()      #通信の後始末
