import glob

class PomFetcherFolder:
    def __init__(self, folder_path, max_items_to_read, pom_found_subject):
        self._pom_filepath_list = self._getPomListFromFolder(folder_path, max_items_to_read)
        self._pom_found_subject = pom_found_subject

    def _getPomListFromFolder(self, folder_path, max_items_to_read):
        pom_list = glob.glob(folder_path +"*.xml")
        return pom_list[0:max_items_to_read]

    def fetch(self):
        for filepath in self._pom_filepath_list:
            data = open(filepath, "r").read()
            self._pom_found_subject.notify_observers(data)