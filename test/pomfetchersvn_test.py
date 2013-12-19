import unittest
from pomfetchersvn import PomFetcherSvn


class PomFetcherSvnTest(unittest.TestCase):

    max_items_to_read = 5

    def setUp(self):
        self._pom_found_subject = TestPomFoundSubject()
        self._pom_fetcher = PomFetcherSvn('http://svn/repo/something', self.max_items_to_read, self._pom_found_subject)

    def tearDown(self):
        self._pom_fetcher = None
        self._pom_found_subject = None

    def test_crawl_finds_expected_number_of_poms(self):
        self._pom_fetcher.crawl()
        self.assertEqual(len(self._pom_found_subject.get_contents()), self.max_items_to_read)

class TestPomFoundSubject:

    def __init__(self):
        self._content = []

    def get_contents(self):
        return self._content

    def notify_observers(self, pom_content):
        self._content.append(pom_content)

if __name__ == '__main__':
    unittest.main()