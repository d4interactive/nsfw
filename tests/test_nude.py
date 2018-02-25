import unittest
import logging

logging.basicConfig(level=logging.INFO)

from nsfw.nude import ProfanityCheck, BagOfWords


class TestNudeChecker(unittest.TestCase):
    """A test case to verify the nude checking by its titles."""

    def setUp(self):
        self.sentences = [
            'Sensual tease leads to passionate fuck anal',
            'Luscious babe seduced her lover',
            'Beautiful girl sensual suck',
            'Diving into Kayden Kross',
            "She so sexy he doesnt last long",
            "Horny brunette japanese takes cock in her hairy cunt",
            "Hot Wife Orgasm Loud From Getting Pussy Fucked All Ways"
        ]

    def test_score(self):
        score = ProfanityCheck.score(self.sentences[0])
        if score:
            assert True

    def test_calculate_collectively(self):
        combined_score = 0
        for sentence in self.sentences:
            score = ProfanityCheck.score(sentence)
            combined_score += score

        total = combined_score / len(self.sentences)
        self.assertGreater(total, 30)

    def test_domain(self):
        result = ProfanityCheck.domain('zbiornik.com')
        self.assertEqual(result, True)

        result = ProfanityCheck.domain('contentstudio.io')
        self.assertEqual(result, False)

        result = ProfanityCheck.domain('cialiswork.com')
        self.assertEqual(result, True)


class TestBOG(unittest.TestCase):
    """A test case for the BOG related work. The way we are generating the bag of words for the filters."""

    def setUp(self):
        self.bog = BagOfWords()

    def test_common_words(self):
        self.bog.common()

    def test_bigrams(self):
        self.bog.bigrams()

    def test_bigram_lines(self):
        self.bog.bigram_to_dict()

    def test_string(self):
        self.bog.string_to_dict()
