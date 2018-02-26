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
        self.non_adult_sentences = [
            "The scientific, efficient way to learn languages: “spaced repetition”",
            "In defense of cream cocktails",
            "Riots, “Real Housewives,” and sexual harassment—the week in bad cruise news",
            "JPMorgan is scrapping its 52-story Manhattan skyscraper in the largest voluntary demolition ever",
            "Dear America, here’s how other countries stop mass shootings",
            "The subconscious sexism of today’s feminist movement",
            "Schools and teachers should teach writing class the same way they teach math class — Quartz",
            "Canada has forgotten its worst mass murder: the 1985 Air India bombing",
            "Watch teens organize against guns in their native language: Snapchat",
            "Talking about gun control without passing laws is actually great for gun makers"]

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

    def test_non_adult(self):
        total_score = 0
        for sentence in self.non_adult_sentences:
            score = ProfanityCheck.score(sentence)
            total_score += score
        self.assertEqual(total_score, 0.0)

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
