import os
import sys
import unittest

from streamparser import parse, SReading, known

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

import apertium  # noqa: E402


class TestAnalyze(unittest.TestCase):

    analyzer = apertium.Analyzer()

    def test_en(self):
        lexical_units = analyzer.analyze('en', 'cats')
        lexical_unit = lexical_units[0]
        self.assertListEqual(lexical_unit.readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            analyzer.analyze('spa', 'cats')


class TestGenerate(unittest.TestCase):

    generator = apertium.Generator()

    def test_single(self):
        wordform = generator.generate('en', '^cat<n><pl>$')
        self.assertEqual(wordform, 'cats')

    def test_multiple(self):
        lexical_units = generator.generate('en', '^cat<n><pl>$ ^cat<n><pl>$')
        self.assertEqual(lexical_units, 'cats cats')

    def test_bare(self):
        lexical_units = generator.generate('en', 'cat<n><pl>')
        self.assertEqual(lexical_units, 'cat<n><pl>')

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            generator.generate('spa', 'cat<n><pl>')


class TestTranslate(unittest.TestCase):

    translator = apertium.Translator()

    def test_en_spa(self):
        translated = translator.translate('eng', 'spa', 'cats')
        self.assertEqual(translated, 'Gatos')
