import glob

class PomFetcherFolder:
    def __init__(self, folder_path, max_items_to_read):
        self._pom_filepath_list = self._getPomListFromFolder(folder_path, max_items_to_read)
        self._current_index = 0

    def _getPomListFromFolder(self, folder_path, max_items_to_read):
        pom_list = glob.glob(folder_path +"*.xml")
        return pom_list[0:max_items_to_read]

    def number_of_poms(self):
        return len(self._pom_filepath_list)

    def has_next(self):
        return self._current_index < self.number_of_poms()

    def get_pom_contents(self):
        pom_filepath = self._pom_filepath_list[self._current_index]
        data = open(pom_filepath, "r").read()
        self._current_index += 1
        return data