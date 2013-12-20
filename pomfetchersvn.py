import re

class PomFetcherSvn:
    def __init__(self, opener, root_path, max_items_to_read, pom_found_subject, logger):
        self._root_path = root_path
        self._pom_found_subject = pom_found_subject
        self._opener = opener
        self._max_items = max_items_to_read
        self._found_items = 0
        self._logger = logger

        #TODO configure blacklist?
        self._blacklist = ["../", "./", "LiveStats/", "src/", "target/"]

    def fetch(self):
        self.crawl(self._root_path)
        self._log("FOUND %i pom.xml files" % (self._found_items))
        if self._found_items >= self._max_items:
            self._log('reached max number of poms')
            return

    def crawl(self, uri):
        if self._found_items >= self._max_items:
            return
        self._log('crawling: ' + uri)

        try:
            if self._pom_exists(uri):
                pom_content = self._get_pom_contents(uri)
                self._pom_found_subject.notify_observers(pom_content)
                self._found_items += 1
            subFolders = self._get_sub_folders(uri)
            for subFolder in subFolders:
                self.crawl(subFolder)
        except Exception, e:
            print('exception', e)
        return

    def _pom_exists(self, uri):
        folder = self._opener.open(uri)
        for line in folder:
            if 'pom.xml' in line:
                self._log('FOUND POM in ' + uri)
                return True
        return False

    def _get_pom_contents(self, uri):
        pomUri = uri + 'pom.xml'
        urlinfo = self._opener.open(str(pomUri))
        return urlinfo.read()

    def _get_sub_folders(self, uri):
        subDirectories = []
        try:
            folder = self._opener.open(uri)
        except:
            self._log('URLError occured using uri ' + uri)
            return subDirectories

        foundSubdirectories = []
        for line in folder:
            sub_directory = re.search("href=\".+/\">", line)
            if not sub_directory == None:
                foundSubdirectories.append(sub_directory)

        for found_sub_directory in foundSubdirectories:
            subdir = found_sub_directory.group(0)[6:-2]
            if (not subdir.startswith('.')) and (subdir not in self._blacklist):
                subDirectories.append(uri + subdir)
        return subDirectories

    def _log(self, message):
        if not self._logger == None:
            self._logger.log(message)