class Engine:

    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, subscriber_id, topic, receive_callback):

        # If it is a new topic
        if topic not in self.subscriptions:
            self.subscriptions[topic] = {}

        # Save the listener callback
        self.subscriptions[topic][subscriber_id] = receive_callback

    def unsubscribe(self, subscriber_id, topic):

        # If topic exists
        if topic in self.subscriptions:
            # If subscriber_id is a listener in the topic
            if subscriber_id in self.subscriptions[topic]:
                # Remove from the list
                del self.subscriptions[topic][subscriber_id]

    def inject(self, event):

        # List all callbacks functions subscribed in event.topic
        if event.topic in self.subscriptions:
            for callback in self.subscriptions[event.topic].values():

                # Call the function
                callback(event)
