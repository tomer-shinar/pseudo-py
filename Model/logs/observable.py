class Observable:
    """
    this is a class for observable items according to observer design pattern.
    """
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        """
        add one listener or a list of listeners
        :param listener: one or more observer/s
        """
        if isinstance(listener, list):
            # listener is actually few listeners
            self.listeners += listener
        else:
            self.listeners.append(listener)

    def notify(self, event, *args, **kwargs):
        """
        notify all listeners about event
        :param event: event to notify about
        :param args: data about event
        :param kwargs: data about event
        """
        for listener in self.listeners:
            listener.update(self, event, *args, **kwargs)

    def remove_listener(self, listener):
        """
        remove listener
        :param listener: listener to remove
        """
        if listener in self.listeners:
            self.listeners.remove(listener)
        else:
            raise Exception("no such listener")
