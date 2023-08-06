- **Thư viện Consumer của JB. Chạy consumer ở Process, phù hợp cho môi trường K8s** :

- **NOTE: SDK sử dụng confluent-kafka depend requirements của module. SDK không có install_requires confluent-kafka :)** ::cheers::
# create topic
Note:
- EnsureKafkaTopic.REPLICATION_ASSIGNMENT là giá trị các brokers isolate của từng module. Nếu giá trị này chưa được DevOps khởi tạo nó sẽ được lấy giá trị từ *DEFAULT_BROKER_ID_ASSIGN*  
```python
from mobio.libs.kafka_lib.helpers.ensure_kafka_topic import EnsureKafkaTopic
import os
from mobio.libs.kafka_lib import MobioEnvironment

EnsureKafkaTopic().create_kafka_topics(
        [
            # TEST WITH SET replica_assignment
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test1",
                EnsureKafkaTopic.NUM_PARTITIONS: 8,
                EnsureKafkaTopic.CONFIG: {"compression.type": "snappy"},
                EnsureKafkaTopic.REPLICATION_ASSIGNMENT: os.getenv(
                    MobioEnvironment.SALE_BROKER_ID_ASSIGN # SALE_BROKER_ID_ASSIGN
                ) # danh sách các broker_ids "10,20,30" ,
            },
            # TEST WITH SET replica_factor
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test2",
                EnsureKafkaTopic.REPLICATION_FACTOR: 3,
            },
            # TEST WITH SET config
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test3",
                EnsureKafkaTopic.NUM_PARTITIONS: 1,
                EnsureKafkaTopic.CONFIG: {"compression.type": "snappy"},
            },
            # TEST WITHOUT manual config
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test4",
                EnsureKafkaTopic.NUM_PARTITIONS: 1,
            },
        ]
    )
```


# Producer
```python
from mobio.libs.kafka_lib.helpers.kafka_producer_manager import KafkaProducerManager
KafkaProducerManager().flush_message(topic="test", key="uuid", value={"test":1})
```

# Consumer
```python
import os
from time import sleep
from pymongo import MongoClient
from mobio.libs.kafka_lib.helpers.kafka_consumer_manager import BaseKafkaConsumer


class TestConsumer(BaseKafkaConsumer):
    def message_handle(self, data):
        print("TestConsumer: data: {}".format(data))


if __name__ == "__main__":
    url_connection = os.getenv('TEST_MONGO_URI')
    client_mongo = MongoClient(url_connection, connect=False)

    TestConsumer(topic_name="test", group_id="test", client_mongo=client_mongo, retryable=False)
    sleep(1000)
```

# change logs
* 0.1.4.2 (2022-09-19):
    * fix bug topic được tạo đang random vào cả các broker isolate cho module khác.
* 0.1.4.1 (2022-09-19):
    * cho phép truyền vào brokers mà topic này sẽ được replicate
* 0.1.4 (2022-08-23):
    * Bổ sung thêm phần lưu mapping pod-name và client-id vào file 
* 0.1.3:
   * Mặc định compress messages ở đầu producer
   * Function create kafka topic hỗ trợ truyền số partitions và settings của topic  

* 0.1.1: fix bug init Config