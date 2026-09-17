"""Fresh teaching builds skip retired cells without removing active code."""
import unittest

import nbformat

from execute_notebook import skip_archived_cells


class TeachingExecutionTests(unittest.TestCase):
    def test_retired_cells_are_skipped(self):
        notebook = nbformat.v4.new_notebook(cells=[
            nbformat.v4.new_code_cell("raise RuntimeError('retired')",
                                     metadata={"tags": ["archive-only"]}),
            nbformat.v4.new_code_cell("raise RuntimeError('removed')",
                                     metadata={"tags": ["remove-cell"]}),
            nbformat.v4.new_code_cell("value = 4"),
        ])
        self.assertEqual([cell.source for cell in skip_archived_cells(notebook).cells],
                         ["value = 4"])

    def test_reader_and_slide_dependencies_are_kept(self):
        cells = [nbformat.v4.new_code_cell("value = 4", metadata={"tags": [tag]})
                 for tag in ["reader-only", "slides-only", "hide-input"]]
        notebook = nbformat.v4.new_notebook(cells=cells)
        self.assertEqual(len(skip_archived_cells(notebook).cells), 3)

    def test_active_cell_order_is_unchanged(self):
        notebook = nbformat.v4.new_notebook(cells=[
            nbformat.v4.new_code_cell("first = 1"),
            nbformat.v4.new_markdown_cell("Retired", metadata={"tags": ["archive-only"]}),
            nbformat.v4.new_code_cell("second = first + 1"),
        ])
        self.assertEqual([cell.source for cell in skip_archived_cells(notebook).cells],
                         ["first = 1", "second = first + 1"])


if __name__ == "__main__":
    unittest.main()
