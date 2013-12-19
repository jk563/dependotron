
class PomFetcherSvn:
    def __init__(self, root_path, max_items_to_read):
        self._current_path = root_path

    def has_next(self):
        return False

    def get_pom_contents(self):
        return None