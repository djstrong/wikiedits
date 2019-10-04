import unittest
import os
import gzip
import json

from wikiedits.wiki_edit_extractor import WikiEditExtractor

MODULE_PATH = os.path.dirname(__file__)
META_DATA_PATH = os.path.join(MODULE_PATH, "verified_meta_values.json")


class WikiEditExtractorTest(unittest.TestCase):

    WIKI_TEMP_FILE = "enwiki.temp.xml"

    def setUp(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data",
                                 "enwiki-20140102.tiny.xml.gz")

        dump = gzip.open(file_name, "rb")
        with open(self.WIKI_TEMP_FILE, "w") as file:
            file.write(dump.read())
        dump.close()

        self.wiki = WikiEditExtractor(
            self.WIKI_TEMP_FILE,
            lang='english',
            min_words=3,
            max_words=120,
            length_diff=4,
            edit_ratio=0.3,
            min_chars=10)

    def tearDown(self):
        os.remove(self.WIKI_TEMP_FILE)

    def test_wiki_extract_edit_meta(self):
        verified_meta_values = json.load(open(META_DATA_PATH))

        for edits, meta in self.wiki.extract_edits():
            verified_meta_value = verified_meta_values.pop(0)
            self.assertDictEqual(meta, verified_meta_value)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
