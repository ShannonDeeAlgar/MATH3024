"""Current narrative checks for the Week 10 Reader and slide source.

These checks deliberately inspect only live cells. Older revision cells are
kept in the notebook with ``remove-cell`` tags, but are not teaching material.
"""
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week10/L_Game_theory.ipynb"


def live_cells(notebook, audience=None):
    excluded = {"remove-cell", "archive-only", "presenter-notes"}
    if audience == "reader":
        excluded.add("slides-only")
    elif audience == "slides":
        excluded.add("reader-only")
    return [cell for cell in notebook["cells"]
            if not set(cell.get("metadata", {}).get("tags", [])) & excluded]


class ReaderFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text())
        cls.reader = live_cells(cls.notebook, "reader")
        cls.slides = live_cells(cls.notebook, "slides")
        cls.reader_ids = [cell["id"] for cell in cls.reader]
        cls.slide_ids = [cell["id"] for cell in cls.slides]
        cls.reader_sources = {cell["id"]: "".join(cell.get("source", [])) for cell in cls.reader}
        cls.all_sources = {cell["id"]: "".join(cell.get("source", []))
                           for cell in cls.notebook["cells"]}

    def test_no_duplicate_live_ids(self):
        self.assertEqual(len(self.reader_ids), len(set(self.reader_ids)))
        self.assertEqual(len(self.slide_ids), len(set(self.slide_ids)))

    def test_core_sequence(self):
        sequence = [
            "w10-rps-local-game", "d9bf6664", "8309b600-a5e3-4836-853a-d685bf85dd2f",
            "185e0fc7-41d0-47a3-b5e9-cdedc9619297", "e190c160-09b7-46d5-8983-6aa6f397daf4",
            "c1cd393a-fb79-4969-886d-91559cef052a", "w10-analysis-banner",
            "894680c8-6d78-4117-b994-6b42b5c64ffe", "b091f920-71fa-423d-bcca-802cdfc18199",
            "w10-comparing-game-types", "09fa3a4f", "w10-evolution-bridge",
            "w10-payoff-to-fitness", "w10-tournament-field-distribution",
            "a7e5e594", "w10-rps-population",
        ]
        positions = [self.reader_ids.index(cell_id) for cell_id in sequence]
        self.assertEqual(positions, sorted(positions))

    def test_live_heading_hierarchy_has_no_skips(self):
        previous = 1
        first = True
        for cell in self.reader:
            for match in re.finditer(r"^(#{1,6})\s+", "".join(cell.get("source", [])), re.M):
                level = len(match.group(1)) + 1  # Reader page title occupies H1.
                if first:
                    first = False
                else:
                    self.assertLessEqual(level, previous + 1, cell["id"])
                previous = level

    def test_action_profiles_precede_payoffs_and_analysis(self):
        self.assertLess(self.reader_ids.index("185e0fc7-41d0-47a3-b5e9-cdedc9619297"),
                        self.reader_ids.index("e190c160-09b7-46d5-8983-6aa6f397daf4"))
        self.assertLess(self.reader_ids.index("e190c160-09b7-46d5-8983-6aa6f397daf4"),
                        self.reader_ids.index("w10-analysis-banner"))

    def test_pd_analysis_is_split_and_generalised(self):
        dominance = self.reader_sources["894680c8-6d78-4117-b994-6b42b5c64ffe"]
        nash = self.reader_sources["b091f920-71fa-423d-bcca-802cdfc18199"]
        self.assertTrue(dominance.startswith("#### Dominance"))
        self.assertIn("Nash equilibrium", self.all_sources["b091f920-71fa-423d-bcca-802cdfc18199-notation-slide"])
        self.assertIn("throughout this analysis", self.reader_sources["f328572a"].lower())
        self.assertIn("T>R>P>S", self.reader_sources["a8733185-a037-45a2-b04e-75ac43cedb98"])

    def test_comparison_and_atlas_are_before_repeated_play(self):
        self.assertLess(self.reader_ids.index("w10-comparing-game-types"), self.reader_ids.index("09fa3a4f"))
        self.assertLess(self.reader_ids.index("09fa3a4f"), self.reader_ids.index("w10-evolution-bridge"))
        atlas = self.reader_sources["09fa3a4f"]
        self.assertIn("Each $2\\times2$ game", atlas)
        self.assertIn("S$, $P$, $R$ and $T$", atlas)
        self.assertIn("rank pairs", self.all_sources["w10-atlas-reading-slide"])

    def test_tournament_and_evolution_are_distinguished(self):
        tournament = self.reader_sources["w10-payoff-to-fitness"]
        evolution = self.reader_sources["w10-tournament-field-distribution"]
        summaries = tournament + self.reader_sources["week10-pathway"]
        self.assertIn("no strategy is copied", tournament.lower())
        self.assertIn("one round is one prisoner’s dilemma encounter", summaries.lower())
        self.assertIn("strategy rules fixed", evolution.lower())
        self.assertIn("between generations", evolution.lower())
        self.assertIn("2,000 agents", evolution)
        self.assertIn("80 independent 50-round matches", evolution)

    def test_tournament_notation_defines_round_match_and_axis(self):
        reader = self.reader_sources["w10-payoff-to-fitness"]
        self.assertIn("one round is one simultaneous Prisoner’s Dilemma encounter", reader)
        self.assertIn("One repeated match is 50 rounds", reader)
        self.assertIn("A tournament is 300 such matches", reader)
        self.assertIn("completed tournament matches", reader)
        self.assertIn("Heatmap cells average 30 independent 50-round matches", reader)

    def test_population_extensions_have_explicit_model_headings(self):
        for cell_id, phrase in (("a7e5e594", "static population"),
                                ("w10-rps-population", "moving population")):
            self.assertIn(phrase, self.reader_sources[cell_id].lower())
        live = "\n".join(self.reader_sources.values())
        self.assertNotIn("optional-reader-flag", live)
        self.assertNotIn("Other strategic settings", live)

    def test_figures_are_numbered_and_assets_exist(self):
        reader = "\n".join(self.reader_sources.values())
        for number in range(1, 9):
            self.assertIn(f"fig-w10-{number}", reader)
        for asset in ("rps_cyclic_dominance.svg", "pd_best_response_plane.svg",
                      "game_type_best_response_arrows.svg", "atlas_pd_105.svg",
                      "axelrod_tournament_random_opponents.svg", "axelrod_evolution_dynamics.svg",
                      "axelrod_reference/all_strategies_boxplot.svg",
                      "axelrod_reference/all_strategies_payoff.svg",
                      "axelrod_reference/all_strategies_reproduce.svg"):
            self.assertTrue((ROOT / "notebooks/week10/images" / asset).exists(), asset)

    def test_removed_material_is_not_live(self):
        live = "\n".join(self.reader_sources.values())
        self.assertNotIn("Evolution in action: tracking strategy frequencies", live)
        self.assertNotIn("Structured populations", live)
        self.assertNotIn("Other strategic settings", live)
        self.assertNotIn("Read one payoff entry", live)


class PracticeFormattingTests(unittest.TestCase):
    def test_practice_question_sections_are_simple_and_explicit(self):
        practice = (ROOT / "notebooks/week10/Practice.md").read_text()
        self.assertIn("## Optional extensions", practice)
        self.assertNotIn("## Core questions", practice)
        self.assertNotIn("Questions 6, 7 and 9 are optional", practice)
        self.assertNotIn("### 2a.", practice)
        self.assertNotIn("### 9a.", practice)
        self.assertIn("Example solution", practice)
        core = practice.split("## Optional extensions", 1)[0]
        self.assertEqual(re.findall(r"^(\d+)\. ", core, re.M), ["1", "2", "3", "4", "5", "6", "7"])
        optional = practice.split("## Optional extensions", 1)[1]
        self.assertEqual(re.findall(r"^(\d+)\. ", optional, re.M), ["1", "2", "3", "4", "5", "6"])


if __name__ == "__main__":
    unittest.main()
