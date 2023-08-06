
from retrying import retry
import json
from pika import BlockingConnection, URLParameters
from intelab_python_tool.tools.connect import ConnectError
from intelab_python_tool.tools.log import log


def producer(rabbitmq_config: dict, msg_list: list, queue_name: str) -> None:
    """
    rabbitmq生产者，注意msg_list为list, 其中包含的数据应该为dict
    使用方式如下：

    from intelab_python_tool.tools.connect.Rabbitmq import producer
    producer(rabbitmq_config, msg_list, queue_name)

    :param rabbitmq_config:
    :param msg_list:
    :param queue_name:
    :return:
    """
    connection = _connect(rabbitmq_config)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    for msg in msg_list:
        if not isinstance(msg, dict):
            raise ConnectError("msg必须是dict")
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(msg, ensure_ascii=False))
    channel.close()


def consumer(rabbitmq_config: dict, queue_name: str, alarm: any) -> any:
    """
    rabbitmq的消费者，注意log和alarm，log是用来记录日志的对象，alarm则是发送警告的函数对象
    使用方法如下：

    from intelab_python_tool.tools.connect.Rabbitmq import consumer
    rabbitmq_consumer = consumer(rabbitmq_config, queue_name, log, alarm)

    @rabbitmq_consumer
    def consume(ch, method, properties, body):
        这里是对传来的mq_json, 具体消费的自定义相关操作
       ...
        log.info('消息为{}'.format(body))
        body = json.loads(body)
        if body['type'] == 'test':
            print(body['content'])

        ch.basic_ack(delivery_tag=method.delivery_tag)


    :param rabbitmq_config:
    :param queue_name:
    :param alarm:
    :return:
    """
    connection = _connect(rabbitmq_config)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    def _in_func(function):

        channel.basic_qos(prefetch_count=1)  # 类似权重，按能力分发，如果有一个消息，就不在给你发
        channel.basic_consume(  # 消费消息
            queue=queue_name,  # 要消费的队列
            on_message_callback=function  # 如果收到消息，就调用callback函数来处理消息
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            log.info('MQ connection closed by user')
            pass
        except Exception as e:
            log.exception('MQ connection closed unexpectedly. %s', e)
            # TODO 通知到开发者
            alarm(e)
            raise

    return _in_func


@retry(stop_max_attempt_number=3, wait_random_min=100, wait_random_max=1000)
def _connect(rabbitmq_config: dict) -> any:
    
    if rabbitmq_config.get("HOST"):
        format_rabbitmq_config = {
            'host': rabbitmq_config.get("HOST"),
            'port': rabbitmq_config.get("PORT"),
            'user': rabbitmq_config.get("USERNAME"),
            'password': rabbitmq_config.get("PASSWORD"),
            'database': rabbitmq_config.get("DATABASE"),
            'heartbeat': rabbitmq_config.get("HEARTBEAT")
        }
    else:
        format_rabbitmq_config = rabbitmq_config

    connection = BlockingConnection(
        URLParameters('amqp://{user}:{password}@{host}:{port}/%2f?heartbeat={heartbeat}'.format(**format_rabbitmq_config)))

    return connection


if __name__ == '__main__':

    rabbitmq_config = {"user": 'ilabservice', "password": 'iLabServiceOps123456',
                       "host": '47.101.208.180', "port": 32060, "heartbeat": 600}

    # msg_list = [{"type": "test", "content": "here is just a test"}]
    #
    # print("start to send mq")
    # try:
    #     producer(rabbitmq_config, msg_list, "RECOMPUTING_UTILIZATION")
    # except Exception as e:
    #     print("lose to send mq-msg")
    #
    print("start to consume mq")

    def alarms(e):
        print(e)


    try:
        cons = consumer(rabbitmq_config, "RECOMPUTING_UTILIZATION", alarms)

        @cons
        def callback(ch, method, properties, body):

            log.info('消息为{}'.format(body))
            body = json.loads(body)
            if body['type'] == 'test':
                print(body['content'])

            ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成
    except Exception as e:
        alarms(e)

