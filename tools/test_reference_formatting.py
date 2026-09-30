import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from check_reference_formatting import check


class ReferenceFormattingTests(unittest.TestCase):
    def errors_for(self, citation):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'page.json').write_text(json.dumps({'references': {'cite': {'data': {
                'example': {'doi': '10.example/test', 'html': citation}
            }}}}))
            return check(root)[0]

    def test_capitals_are_flagged_only_in_names(self):
        self.assertTrue(self.errors_for('SMITH, J., & PRICE, G. (1973). Title. <i>Nature</i>.'))
        self.assertFalse(self.errors_for('Stützle, T., & Hoos, H. H. (2000). MAX–MIN Ant System. <i>Journal</i>.'))

    def test_editor_and_compound_name_are_valid(self):
        self.assertFalse(self.errors_for('Adamatzky, A. (Ed.). (2010). <i>Game of Life cellular automata</i>. Springer.'))
        self.assertFalse(self.errors_for('Maynard Smith, J., & Price, G. R. (1973). Title. <i>Nature</i>.'))

    def test_incomplete_metadata_is_flagged(self):
        self.assertTrue(self.errors_for('Hutchinson, J. (1981). <i>Indiana University Mathematics Journal</i>.'))
        self.assertTrue(self.errors_for('Kuramoto, Y. (n.d.). Self-entrainment.'))
        self.assertTrue(self.errors_for('Stützle, T. (2000). – Ant System.'))


if __name__ == '__main__':
    unittest.main()
