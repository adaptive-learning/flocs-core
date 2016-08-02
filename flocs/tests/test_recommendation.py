import unittest
from recommendation import recommend_task


class TestRecommendation(unittest.TestCase):

    def setUp(self):
        self.student = 'Lojza', #Student()
        self.tasks = ['zig-zag'], #[Task()]


    def test_recommend_single_task(self):
        self.assertEqual(
            recommend_task(self.student, [self.tasks[0]], criteria=[]),
            self.tasks[0]
        )
