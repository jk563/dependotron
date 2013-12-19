
class PomFetcherSvn:
    def __init__(self, root_path, max_items_to_read, pom_found_subject):
        self._current_path = root_path
        self._pom_found_subject = pom_found_subject

    def fetch(self):
        # recurse through svn. call self._pom_found_subject.notify_observers(pom_contents) when pom found
        pass
