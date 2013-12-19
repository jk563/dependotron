import unittest
from pomfetcherfolder import PomFetcherFolder


class PomFetcherFolderTest(unittest.TestCase):

    max_items_to_read = 1

    def setUp(self):
        self._pom_found_subject = TestPomFoundSubject()
        self._pom_fetcher = PomFetcherFolder('resources/xml/', self.max_items_to_read, self._pom_found_subject)

    def tearDown(self):
        self._pom_fetcher = None
        self._pom_found_subject = None

    def test_crawl_finds_expected_number_of_poms(self):
        self._pom_fetcher.fetch()
        self.assertEqual(len(self._pom_found_subject.get_contents()), self.max_items_to_read)

    def test_crawl_returns_some_content(self):
        self._pom_fetcher.fetch()
        contents = self._pom_found_subject.get_contents()[0]
        self.assertTrue(contents.startswith("<?xml version=\"1.0\"?>\n<project xmlns=\"http://maven.apache.org/POM/"))

class TestPomFoundSubject:

    def __init__(self):
        self._content = []

    def get_contents(self):
        return self._content

    def notify_observers(self, pom_content):
        self._content.append(pom_content)

if __name__ == '__main__':
    unittest.main()