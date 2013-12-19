"""
Subject class that registers observers of a pom files contents
"""
class PomFoundSubject:

    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        # check observer has update method taking single string
        try:
            if observer.update and not observer in self.observers:
                self.observers.append(observer)
        except AttributeError:
            return


    def unregister_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    """
    Pass the contents of a pom (as a string) to all registered observers
    """
    def notify_observers(self, pomContents):
        for observer in self.observers:
            observer.update(pomContents)