import unittest
from pomfetchersvn import PomFetcherSvn


class PomFetcherSvnTest(unittest.TestCase):

    max_items_to_read = 5

    def setUp(self):
        self._pom_fetcher_folder = PomFetcherSvn('http://svn/repo/something', self.max_items_to_read)

    def tearDown(self):
        self._pom_fetcher_folder = None

    def test_has_next_returns_true_then_false_after_reading_pom_contents(self):
        for i in range(self.max_items_to_read):
            self.assertTrue(self._pom_fetcher_folder.has_next())
            self._pom_fetcher_folder.get_pom_contents()

        self.assertFalse(self._pom_fetcher_folder.has_next())

    def test_get_pom_contents_returns_some_content(self):
        contents = self._pom_fetcher_folder.get_pom_contents()
        self.assertTrue(contents.startswith("<?xml version=\"1.0\"?>\n<project xmlns=\"http://maven.apache.org/POM/"))

    def test_repeated_calls_to_get_pom_contents_are_safe(self):
        for i in range(self.max_items_to_read):
            self._pom_fetcher_folder.get_pom_contents()

        contents = self._pom_fetcher_folder.get_pom_contents()
        self.assertIsNone(contents)

if __name__ == '__main__':
    unittest.main()