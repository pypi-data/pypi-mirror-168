class Event:

    def __init__(self, topic, timestamp, partition, value):

        self.topic = topic
        self.timestamp = timestamp
        self.partition = partition
        self.value = value
