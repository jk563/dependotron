import unittest
from pomfetcherfolder import PomFetcherFolder


class PomFetcherFolderTest(unittest.TestCase):

    max_items_to_read = 1

    def setUp(self):
        self._pom_fetcher_folder = PomFetcherFolder('resources/xml/', self.max_items_to_read)

    def tearDown(self):
        self._pom_fetcher_folder = None

    def test_PomFetcherFolder_has_next_returns_true_then_false_after_reading_pom_contents(self):
        self.assertEqual(self._pom_fetcher_folder.number_of_poms(), self.max_items_to_read)

        self.assertTrue(self._pom_fetcher_folder.has_next())

        self._pom_fetcher_folder.get_pom_contents()

        self.assertFalse(self._pom_fetcher_folder.has_next())

    def test_PomFetcherFolder_returns_some_content(self):
        contents = self._pom_fetcher_folder.get_pom_contents()
        #print contents
        self.assertTrue(contents)

if __name__ == '__main__':
    unittest.main()