import unittest
from pomfoundsubject import PomFoundSubject


class PomFoundSubjectTest(unittest.TestCase):

    test_content = "some pom content"

    def setUp(self):
        self._pom_found_subject = PomFoundSubject()
        self._test_observer = TestPomFoundObserver()

    def tearDown(self):
        self._pom_found_subject = None

    def test_single_observer_called_with_correct_content(self):
        self._pom_found_subject.register_observer(self._test_observer)
        self._pom_found_subject.notify_observers(self.test_content)
        self.assertEquals(self.test_content, self._test_observer.get_content())

    def test_observer_can_be_unregistered(self):
        self._pom_found_subject.register_observer(self._test_observer)
        self._pom_found_subject.unregister_observer(self._test_observer)
        self._pom_found_subject.notify_observers(self.test_content)
        self.assertIsNone(self._test_observer.get_content())

    def test_non_observers_not_registered(self):
        self._pom_found_subject.register_observer(TestNotPomFoundObserver())
        self._pom_found_subject.register_observer(None)
        self._pom_found_subject.notify_observers(self.test_content)

class TestPomFoundObserver:

    def __init__(self):
        self._content = None

    def update(self, pom_contents):
        self._content = pom_contents

    def get_content(self):
        return self._content

class TestNotPomFoundObserver:
    pass

if __name__ == '__main__':
    unittest.main()