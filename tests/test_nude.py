import unittest
import logging

logging.basicConfig(level=logging.INFO)

from nsfw.nude import ProfanityCheck


class TestNudeChecker(unittest.TestCase):
    def setUp(self):
        self.sentences = [
            'Sensual tease leads to passionate fuck',
            'Luscious babe seduced her lover',
            'Beautiful girl sensual suck',
            'Diving into Kayden Kross'
        ]

    def test_score(self):
        score = ProfanityCheck.score(self.sentences[0])
        print(score)
