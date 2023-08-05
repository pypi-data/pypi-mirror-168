from datetime import datetime
from tkinter import SEL_FIRST


class Event:

    from datetime import datetime

    def __init__(self, timestamp, topic, partition, value):

        self.timestamp = timestamp
        self.topic = topic
        self.partition = partition
        self.value = value

    def __repr__(self):
        return '{} - {}/{}: {}'.format(self.timestamp, self.topic, self.partition, self.value)
